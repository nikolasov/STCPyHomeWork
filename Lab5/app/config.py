from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    class Config:
        env_file = './.env'


settings = Settings()
settings.POSTGRES_DB = 'check_tasks'
settings.DATABASE_PORT = 5432
settings.POSTGRES_USER = 'user1'
settings.POSTGRES_PASSWORD = '123'
settings.POSTGRES_HOSTNAME = 'localhost'
settings.POSTGRES_HOST = '127.0.0.1'
