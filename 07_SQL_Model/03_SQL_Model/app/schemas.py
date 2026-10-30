from pydantic import BaseModel, Field
from app.database.models import ShipmentStatus





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