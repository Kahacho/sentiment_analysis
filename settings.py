from functools import lru_cache

from config import TwitterAPIKeys


@lru_cache()
def twitter_api_keys():
    return TwitterAPIKeys()
