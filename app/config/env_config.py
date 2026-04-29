import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.DB_URL = os.getenv("DB_URL")

        if not self.DB_URL:
            raise ValueError("DB_URL is not set")
        
def get_settings():
    return Settings()

settings = get_settings()