# For reading the env variable from .env file 

# so for it insted of  just loading the file and parsing the env. variable > we can use utility function from pydantic

from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # by this we have defined our fields, that is the environment variables which we wish to read, 
    # we have to point it to environment file as well , and for it we will use config 

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore", #if we have some extra in .env file ignore that (like some custom settings)
    )


    # for database connection url, we can add utility method to database setting class
    @property #if we want to use this postgres_url as an attribute
    def POSTGRES_URL(self):
        return "postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}" # "postgresql+asyncpg://user:password@host:port/db" > since we want to do asynchronous operation on our database so we have added "asyncpg" driver

settings = DatabaseSettings() #now we can use it to read our enviromnet variables
# settings.POSTGRES_URL #We can use it as attribute