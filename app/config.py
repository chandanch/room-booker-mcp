from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    entra_client_id: str = Field(alias="ENTRA_CLIENT_ID")
    entra_client_secret: str = Field(alias="ENTRA_CLIENT_SECRET")
    entra_tenant_id: str = Field(alias="ENTRA_TENANT_ID")

    mcp_base_url: str = Field(
        default="http://localhost:8000",
        alias="MCP_BASE_URL",
    )

    mcp_required_scope: str = Field(
        default="Mcp.Access",
        alias="MCP_REQUIRED_SCOPE",
    )

    server_host: str = Field(
        default="127.0.0.1",
        alias="SERVER_HOST",
    )

    server_port: int = Field(
        default=8000,
        alias="SERVER_PORT",
    )

    mcp_version: str = Field(
        default="0.1.0",
        alias="MCP_VERSION",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
