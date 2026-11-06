from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from app.database.models import ShipmentStatus





#we are repeating the fields, quite lot > so we can use Python inhertance of simple class 

# class BaseShipment(BaseModel):
#     content: str
#     weight: float = Field(le=25)
#     destination: int

class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destination: int




class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime

# NOW WE CAN USE THIS IN EVERY OTHER PLACES AS WELL 

class ShipmentCreate(BaseShipment):
    pass


#we are repeating the fields, quite lot > so we can use Python inhertance of simple class 

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
