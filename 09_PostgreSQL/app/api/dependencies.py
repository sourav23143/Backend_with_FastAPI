
# IT WILL CONTAINS DEPENDENCIES OF OUR ENDPOINTS
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Seller, DeliveryPartner

from app.utils import decode_access_token
from app.core.security import oauth2_scheme_seller, oauth2_scheme_partner
from app.database.session import get_session
from app.database.redis import is_jti_blacklisted
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.services.delivery_partner import DeliveryPartnerService

SessionDep = Annotated[AsyncSession, Depends(get_session)]  # When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it



# Access token data dep
async def _get_access_token(token: str) -> dict:
        data =  decode_access_token(token)


        # Validate the token 
        if data is None or await is_jti_blacklisted(data["jti"]): 
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )

        return data


# Seller access token data
async def get_seller_access_token(token: Annotated[str, Depends(oauth2_scheme_seller)],) -> dict:
     return await _get_access_token(token)
     


# Delivery Partner access token data
async def get_partner_access_token(token: Annotated[str, Depends(oauth2_scheme_partner)],) -> dict:
     return await _get_access_token(token)
     


#Logged In Seller
async def get_current_seller(
          token_data: Annotated[dict, Depends(get_seller_access_token)],
          session: SessionDep,
    ):

    seller =  await session.get(Seller, UUID(token_data["user"]["id"]))

    if seller is None:
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              details = "Not authorized",
         )

    return seller

    
# Logged In Delivery Partner
async def get_current_partner(
          token_data: Annotated[dict, Depends(get_partner_access_token)],
          session: SessionDep,
    ):

    partner =  await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))

    if partner is None:
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              details = "Not authorized",
         )

    return partner



# Seller dep
SellerDep = Annotated[
     Seller,
     Depends(get_current_seller)
]

# Delivery partner dep
DeliveryPartnerDep = Annotated[
     DeliveryPartner,
     Depends(get_current_partner)
]



# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session, DeliveryPartnerService(session))
#and because we not use any await keyword or handle any coroutines during initialization, we can make this normal function as well, because when it is not required we can skip asynchronous part 

# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)


# Delivery Partner service dep
def get_delivery_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)


# Shipment service dep annotation
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

# Seller service dep annotation
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]


# Delivery partner service dep annotaion
DeliveryPartnerServiceDep = Annotated[DeliveryPartnerService , Depends(get_delivery_partner_service)]