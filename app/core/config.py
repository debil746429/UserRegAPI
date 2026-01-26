from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    # for route path
    API_V1_STR: str = "/api/v1"

    # for jwt session token
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    JWT_SECRET: str

    # for refresh token
    REFRESH_TOKEN_EXPIRY_DAYS: int

    # for database connection
    db_host: str
    db_name: str
    db_user: str
    db_password: str = ""

    # email config
    sender_email: EmailStr
    email_password: str

settings = Settings()
