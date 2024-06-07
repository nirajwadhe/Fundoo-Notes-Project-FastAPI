from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file="core/.env")
    DB_URL:str
    SECRET_KEY:str
    ALGORITHM:str

settings = Settings()    
