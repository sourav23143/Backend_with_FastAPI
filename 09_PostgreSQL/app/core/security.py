# HERE WE WILL CREATE SECURITY RELATED STUFF

from fastapi.security import OAuth2PasswordBearer
#OAuth2 flow for authentication using a bearer token obtained with a password when logged in . An instance of it would be used as a dependency to get that bearer token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token") # takes in token url i.e endpoint url from which token are generated 
# and now in turn we can use this as dependency in our route