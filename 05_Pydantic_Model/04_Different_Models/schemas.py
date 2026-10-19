from pydantic import BaseModel, Field
from enum import Enum


class ShipmentStatus(str, Enum): #str makes each enum member a string as well as an enum member.
    placed = "placed"
    transit = "in_transit"
    packed = "packed"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

#we are repeating the fields, quite lot > so we can use Python inhertance of simple class 

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass


#we are repeating the fields, quite lot > so we can use Python inhertance of simple class 

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus