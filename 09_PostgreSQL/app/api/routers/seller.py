from fastapi import APIRouter

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
async def login_seller(email, password) # insted of receiving email and password as query or path parameters, or creatimg a schema, we can use Oauth2 password request form to create a truly OAuth@ password flow