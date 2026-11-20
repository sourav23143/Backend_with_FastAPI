# here we will store redis related connection code

from redis.asyncio import Redis
from app.config import db_settings


Redis(
    host=db_settings.REDIS_HOST,
    port= db_settings.REDIS_PORT,
    db=0,
)

_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0,
)

async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted") #key , value    #adding the jti to blacklist  


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti) #check if that jti exist in blacklisted 