import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.APP_NAME = "API Autopartes Usadas"
        self.APP_VERSION = "1.0.0"
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "mi-super-secret-key")

settings = Settings()