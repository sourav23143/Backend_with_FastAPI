
from datetime import datetime, timedelta
from datetime import timezone, UTC
from uuid import uuid4

from fastapi import HTTPException
import jwt

from app.config import security_settings

def generate_access_token(
                data: dict,
                expiry: timedelta = timedelta(minutes=15)
) -> str:
    
        # JWT Token generation
        return jwt.encode(
            payload={
                **data,
                "jti": str(uuid4()), #Generate a random UUID. # jti key is special key which we use to add any "id" on JWT Token  
                "exp": datetime.now(timezone.utc) + expiry,

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

        # except jwt.ExpiredSignatureError: #Raised when a token's exp claim indicates that it has expired
        #        raise HTTPException(
        #               status_code=401,
        #               detail = "Expired token"
        #     )

        # simply we can catch the JWT error, which is the base exception for all the JWT related error
               
        except jwt.PyJWTError:
              return None