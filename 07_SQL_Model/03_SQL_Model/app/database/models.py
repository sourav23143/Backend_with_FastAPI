from enum import Enum
from datetime import datetime
from sqlmodel import Field, SQLModel  # which we need to inherit to turn a normal Python class into a SQL model compatible with tables inside of our database


class ShipmentStatus(str, Enum): #str makes each enum member a string as well as an enum member.
    placed = "placed"
    transit = "in_transit"
    packed = "packed"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"



class Shipment(SQLModel):
# By default sql model will use class name and convert it lowercase and then use it as our table name 

    # But we can go ahead and define custom one as well > 
    __tablename__ = "shipment"

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25, )
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime  #datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

# BENIFIT OF USING A MODEL LIKE THIS IS NOT TO JUST DEFINE THE TABLE, AS WELL AS USE THIS MODEL TO GET DATA OR SEND DATA TO THE DATABASE AS WELL
# I.E IF WE GET DATA BACK FROM OUR DATABASE SESSION, WE WILL GET IT AS AN INSTANCE OF THIS SHIPMENT CLASS