from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWKS_URL: str = "http://localhost:3000/api/auth/jwks"
    FRONTEND_URL: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"
    OPENAI_API_KEY: str = Field(default="", alias="OPEN_AI_KEY", validation_alias="OPEN_AI_KEY")
    MCP_SERVER_URL: str = "http://localhost:8000/mcp"
    CHATKIT_WORKFLOW_ID: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
