from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mysql_root_password: str = Field(..., env="MYSQL_ROOT_PASSWORD")
    mysql_database: str = Field(..., env="MYSQL_DATABASE")

    class Config:
        env_file = ".env"
        env_prefix = ""


settings = Settings()
