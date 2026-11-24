from typing import Sequence
from fastapi import HTTPException, status

from sqlalchemy import select, any_

from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.database.models import DeliveryPartner, Shipment
from .user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(
            delivery_partner.model_dump()
        )

    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]: # Sequence is jsut a data type that can be iterated just like list
        return  (
            await self.session.scalars(
            select(DeliveryPartner).where(
                zipcode == any_(DeliveryPartner.serviceable_zip_codes) #match zipcode to any of serviceable zipcode inside DeliveryPartner 
                )
            )
        ).all()

    # BY THIS WE HAVE FOUND THE DELIVERY PARTNER WHICH CAN SERVICE A SPECIFIC ZIP CODE AND NOW WE WILL FIND A DELIVERY PARTNER THAT CAN TAKE A SHIPMENT AS WELL I.E DEPENDING ON THEIR HANDLING CAPACITY

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partner_by_zipcode(shipment.destination)

        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment) ##because this is relationship with shipment models ,it back_populates the delivery partner on the shipment as well
                return partner # partner to which shipment is assigned

        # in case we don't find a eligible partner delivering that zipcode or any partner handling capacity reached the maximum limit, we go ahead and raise an error 
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            details = "No delivery partner available"
        )

    async def update(self, partner: DeliveryPartner):
        return await self._update(partner) 


    async def token(self, email, password) -> str:
        return await self._generate_token(email, password)