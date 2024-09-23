import os
# from pydantic_settings import BaseSettin
from dotenv import load_dotenv

load_dotenv()

class Settings():
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:ows1234@db/saas_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "gAfziUeqRfi4xFTlb7R4tieOcWLk3TKUpF37Zfv1Wdk=")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()