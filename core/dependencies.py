"""from functools import lru_cache"""
from core.config import get_settings
from services.glucose_service import GlucoseService


def get_glucose_service() -> GlucoseService:
    settings = get_settings()
    print(settings)
    return GlucoseService(
      settings=settings
    )


""" def get_insight_service() -> InsightService:
    settings = get_settings()
    return InsightService(openai_api_key=settings.openai_api_key)
 """