from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWKS_URL: str = "http://localhost:3000/api/auth/jwks"
    FRONTEND_URL: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
