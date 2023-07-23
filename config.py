from pydantic import BaseSettings


class ConfigModel(BaseSettings):
    class Config:
        env_file = ".env"


class TwitterAPIKeys(ConfigModel):
    # Twitter API keys
    access_token: str
    access_token_secret: str
    consumer_key: str
    consumer_secret: str
    bearer_token: str
