from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()


class EnvConfig(BaseModel):
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "secret_key_default")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    jwt_refresh_token_expire_minutes: int = int(
        os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", "1440")
    )

    database_url: str = os.getenv("DATABASE_URL")

    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))


env_config = EnvConfig()
