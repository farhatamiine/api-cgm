from core.config import Settings
import hashlib
from schemas.glucose import GlucoStatsResponse,GlucoseMetadata,GlucoseRanges,GlucoseStats
from typing import Any,cast,List,Dict
import pandas as pd
import requests

def _calculate_gmi(avg_glucose: float) -> float:
    """Standard clinical GMI formula for mg/dL."""
    return round(3.31 + (0.02392 * avg_glucose), 1)


class GlucoseService:
    def __init__(self,settings:Settings) -> None:
        self.setting = settings
    
    def get_headers(self) -> dict[str,str]:
        api_secret=self.setting.nightscout_secret
        if not api_secret:
            raise ValueError("api_secret is not set.")
        hashed_api_secret = hashlib.sha1(api_secret.encode()).hexdigest()
        return {"api-secret":hashed_api_secret, "Accept": "application/json"}
    


    def fetch_nightscout_data(self,count:int, days:str)->List[Dict[str,Any]]:
        """Fetches raw CGM entries from Nightscout."""
        headers = self.get_headers()
        params: Dict[str,Any]= {
            "count": count,  
            "find[dateString][$gt]": days
        }
        response = requests.get(f"{self.setting.nightscout_url}/api/v1/entries.json", headers=headers, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch data: {response.status_code} - {response.text}")
        
        df = pd.json_normalize(response.json())
        to_drop =  ["noise","filtered","unfiltered","rssi","utcOffset","sysTime"]
        df.drop(columns=to_drop,inplace=True,errors="ignore")
        return cast(List[Dict[str,Any]],df.to_dict(orient="records"))
    
    
    def get_stats(self,count:int, days:str ) -> GlucoStatsResponse:
        records = self.fetch_nightscout_data(count,days)
        """Computes glucostats from raw Nightscout records."""
        if not records:
            raise ValueError("No records provided.")

        values = [int(r["sgv"]) for r in records if r.get("sgv") is not None]
        if not values:
            raise ValueError("No valid glucose values found.")

        total = len(values)
        avg = sum(values) / total

        return GlucoStatsResponse(
            metadata=GlucoseMetadata(period_days=4, total_readings=total),
            stats=GlucoseStats(average=round(avg, 1), gmi=_calculate_gmi(avg)),
            ranges=GlucoseRanges(
                tir=round(sum(1 for v in values if 70 <= v <= 180) / total * 100, 1),
                high=round(sum(1 for v in values if v > 180) / total * 100, 1),
                low=round(sum(1 for v in values if v < 70) / total * 100, 1),
            )
        )