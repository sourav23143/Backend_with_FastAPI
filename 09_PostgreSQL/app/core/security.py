# HERE WE WILL CREATE SECURITY RELATED STUFF

# from typing import Annotated

# from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer
# #OAuth2 flow for authentication using a bearer token obtained with a password when logged in . An instance of it would be used as a dependency to get that bearer token
# from app.utils import decode_access_token

oauth2_scheme_seller = OAuth2PasswordBearer(tokenUrl="/seller/token") # takes in token url i.e endpoint url from which token are generated 
oauth2_scheme_partner = OAuth2PasswordBearer(tokenUrl="/partner/token")
# and now in turn we can use this as dependency in our route

#______________________________________________________________________________________________________________________
# IF NOT USING AUTH TO PASSWORD BEARER
#______________________________________________________________________________________________________________________

# class AccessTokenBearer(HTTPBearer):
#     async def __call__(self, request):
#         # request.headers.get("Authorization").split(" ")[1] # getting second value as token is second in bearer token  # getting authorization details from headers
#         auth_credentials = await super().__call__(request)
#         token = auth_credentials.credentials # if we notice the method that are available for auth_credentails are sam as pydantic, so auth credentials is also pydantic model it self
#     # it is an special method, which take some request and on that request we simply go ahead and provide it to HTTP Bearer call Implemenation and we get back the HTTP authorization credentials

#         token_data = decode_access_token(token)

#         if token_data is None:
#             raise HTTPException(
#                 status_code = 401,
#                 details= "Not authorized!"
#             )
#         return token_data #we can use it as dependency


# access_token_bearer = AccessTokenBearer()

# Annotated[dict, Depends(access_token_bearer)] #if we hit any endpoint with this dependency, it will provide us back access token data

# becuse we have inherited the HTTP bearer, a lot of functionality is also inherited, so if we go and call it's instance i.e this access token bearer,
# we get a method that is already defined 

# access_token_bearer() #it takes in a request and returns the HTTP authorization credentials i.e it just pull out access token or any token in the authorization header, which we can customize as well 
