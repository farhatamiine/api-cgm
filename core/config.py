from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name:str
    app_version: str
    nightscout_url: str
    nightscout_secret:str
    api_key: str
    openai_api_key: str
    model_config = SettingsConfigDict(env_file=".env")
    

@lru_cache()  
def get_settings() -> Settings:
    return Settings() # type: ignore