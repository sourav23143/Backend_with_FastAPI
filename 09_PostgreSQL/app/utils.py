
from datetime import datetime, timedelta

import jwt

from app.config import security_settings

def generate_access_token(
                data: dict,
                expiry: timedelta = timedelta(days=1)
) -> str:
    
        # JWT Token generation
        return jwt.encode(
            payload={
                **data,
                "exp": datetime.now() + expiry,

            },#beacuse we have already validated seller, we don't need password in the payload, Optionally, if we wnat we can use another filed which can be used to expire this jwt token
            
            algorithm=security_settings.JWT_ALGORITHM,
            key= security_settings.JWT_SECRET, # insted of hardcoding them in this JWT encode function, we can pull them out as environment variable, so we can share them later on 
        )


def decode_access_token(token: str) -> dict | None:

        try: 
            return jwt.decode(  #Verify the jwt token signature and return the token claims.
                jwt=token,
                key=security_settings.JWT_SECRET,
                algorithms=[security_settings.JWT_ALGORITHM],
            )
        except jwt.PyJWTError:
              return None