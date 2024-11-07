import os
from dotenv import load_dotenv
from typing import Annotated, Any, Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl


load_dotenv()

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)



class Settings(BaseSettings):
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="allow"
    )
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "0lV9Ya9eDDq+2t2pjQeb6piFVA9L9dxtO+JtlULlub0=")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    def __getattr__(self, name: str):
        return os.getenv(name)

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"


    # @computed_field  # type: ignore[prop-decorator]
    # @property
    def SQLALCHEMY_DATABASE_URI(self, db_name: Optional[str] = None) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.POSTGRES_SCHEME,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=int(self.POSTGRES_PORT),
            path=db_name if db_name else self.POSTGRES_DB,
        )


settings = Settings()