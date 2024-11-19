from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "your_api_key_here"
    BASE_URL: str = "https://api.intrinio.com/v2"

    class Config:
        env_file = ".env"

settings = Settings() 