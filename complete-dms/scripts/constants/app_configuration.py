from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_HOST: str
    API_PORT: int

    DOCKER_SOCK: str
    DOCKER_CLIENT_TIMEOUT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
