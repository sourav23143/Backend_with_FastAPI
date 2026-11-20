
# IT WILL CONTAINS DEPENDENCIES OF OUR ENDPOINTS
from typing import Annotated
from sqlalchemy import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Seller

from app.utils import decode_access_token
from app.core.security import oauth2_scheme
from app.database.session import get_session
from app.database.redis import is_jti_blacklisted
from app.services.shipment import ShipmentService
from app.services.seller import SellerService

SessionDep = Annotated[AsyncSession, Depends(get_session)]  # When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it



# Access token data dep
async def get_access_token(token:Annotated[str, Depends(oauth2_scheme)]) -> dict:
        data =  decode_access_token(token)


        # Validate the token 
        if data is None or await is_jti_blacklisted(data["jti"]): 
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )

        return data


#Logged In Seller
async def get_current_seller(
          token_data: Annotated[dict, Depends(get_access_token)],
          session: SessionDep,
    ):

     return await session.get(Seller, UUID(token_data["user"]["id"]))



# Seller dep
SellerDep = Annotated[
     Seller,
     Depends(get_current_seller)
]


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)
#and because we not use any await keyword or handle any coroutines during initialization, we can make this normal function as well, because when it is not required we can skip asynchronous part 

# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)

# Shipment service dep annotation
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

# Seller service dep annotation
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]