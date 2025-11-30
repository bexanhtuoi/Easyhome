from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # PostgreSQL
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", 5432))
    postgres_db: str = os.getenv("POSTGRES_DB", "mydatabase")
    
    # JWT / CORS
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "").split(",")
    secret_key: str = os.getenv("MY_SECRET_KEY", "secret")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expires_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))

    # Server
    server_host: str = os.getenv("SERVER_HOST", "localhost")
    server_port: int = int(os.getenv("SERVER_PORT", 8000))\

    env: str = os.getenv("ENV", "dev")

settings = Settings()
