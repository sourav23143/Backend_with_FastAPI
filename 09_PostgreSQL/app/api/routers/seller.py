from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from app.database.redis import add_jti_to_blacklist
from app.core.security import oauth2_scheme_seller
from app.utils import decode_access_token
from app.database.models import Seller


from ..schemas.seller import SellerCreate, SellerRead

from ..dependencies import  SellerServiceDep, SessionDep, get_seller_access_token


router = APIRouter(prefix="/seller", tags=["Seller"])

### Register a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep
    ):

    return await service.add(seller)


### Login the seller
@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
    ): # insted of receiving email and password as query or path parameters, or creating a schema, we can use Oauth2 password request form to create a truly OAuth@ password flow

    #using this request_form we can access username and password provided by user(our API Client to perfom a login)
    # this request form is just like our request body, which our JSON object, but a request form is strictly, key-value pair, so we cant have nested value inside it 
    
    # AFTER GETTING THE REQUEST FORM, THAT IS THE LOGIN CREDENTIALS, WE CAN VALIDATE THEM AS WELL AGAINST THE DATA IN OUR DATABASE

    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "type": "jwt",
    }





### logout the seller
@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):  


    await add_jti_to_blacklist(token_data["jti"])

    return {
        "detail": "successfully logged out "
    }
  









# we want to protect the dashboard access to authenticated or only loged in user and for that we need to recieve access token in routehandler, And to do that, we simply need the Oauth2 password bearer and use it as a dependency in our endpoint
# @router.get("/dashboad")
# async def get_dashboard(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     session: SessionDep,
#     ) -> Seller:



#     #valid authenticated user
#     seller = await session.get(Seller, data["user"]["id"])


#     return seller
    # by this we have authenticated user from provided access token, now we can identify them as well from decode data









    # OAuth2PasswordRequestForm is a built-in dependency class in FastAPI that automatically extracts and validates OAuth2 password flow login credentials sent as form data (not JSON)


    # Key Features

    # • Standard Fields: Automatically collects standard OAuth2 fields such as:
	# • username
	# • password
	# • scope / scopes
	# • grant_type
	# • client_id
	# • client_secret


    # • No Manual Parsing: Using form_data: OAuth2PasswordRequestForm = Depends() in a route saves you from declaring individual Form() parameters for username and password.
    # • Swagger UI Compatible: It matches the form-encoded schema required by the OAuth2 specification, making your /token endpoint work out-of-the-box with the "Authorize" button in FastAPI's built-in Swagger UI