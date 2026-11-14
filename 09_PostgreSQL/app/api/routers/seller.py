from typing_extensions import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.seller import SellerCreate, SellerRead

from ..dependencies import  SellerServiceDep


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
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()]
    ): # insted of receiving email and password as query or path parameters, or creating a schema, we can use Oauth2 password request form to create a truly OAuth@ password flow

    #using this request_form we can access username and password provided by user(our API Client to perfom a login)
    # this request form is just like our request body, which our JSON object, but a request form is strictly, key-value pair, so we cant have nested value inside it 
    
    # AFTER GETTING THE REQUEST FORM, THAT IS THE LOGIN CREDENTIALS, WE CAN VALIDATE THEM AS WELL AGAINST THE DATA IN OUR DATABASE












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