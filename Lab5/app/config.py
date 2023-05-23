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


settings = Settings( POSTGRES_DB = 'test'
                    ,DATABASE_PORT = 5432
                    ,POSTGRES_USER = 'psql_user'
                    ,POSTGRES_PASSWORD = str(12345678)
                    ,POSTGRES_HOSTNAME = 'localhost'
                    ,POSTGRES_HOST = '127.0.0.1'  
                    )
