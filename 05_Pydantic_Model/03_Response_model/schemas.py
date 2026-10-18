from pydantic import BaseModel,  Field
from random import randint
#to add custom check for any field
# first we make it a fild, by importing Filed class from Pydantic and assign it to class Shipment Variable
from enum import Enum


def random_destination():
    return randint(11000, 11999)

#_________________________________________________________________________________________________________
#Enum 

class ShipmentStatus(str, Enum):
    placed = "placed"
    transit = "in_transit"
    packed = "packed"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

#_________________________________________________________________________________________________________
    

class Shipment(BaseModel):
    content: str = Field(
        description = "contents of the shipment",
        max_length=30
        ) #by default every filed is a filed 
    weight: float = Field(
        description = "Weight of the shipment in kilograms (Kg)",
        le=25, 
        ge=1
        ) #but when we want extra checks and valiadtion, we can initilize one and provide the check which we want 
    #destination: int | None = Field(default= randint(11000, 11999)) #it is giving fixed default value for all 
    destination: int | None = Field(
        description = "Destination ZipCode. If not provoded will be sent off to a random location",
        default_factory=random_destination) #f we wnat diffrent than we can use default_factory (which take a function and runs it time of creation of shipment model and assigns it the returned value that is our destination) )

    status: ShipmentStatus



# For less than equal to > le
# For less than > ge


#-----------------------------------------------------------------------------------------------------------------------------------------------

# Field(default=...) gets a value, while Field(default_factory=...) gets a function that makes a value when needed.
# destination: int | None = Field(default=randint(11000, 11999))
# Python calls randint(...) when it defines the model class (usually when the module loads). That one number becomes the default for every shipment that omits destination.
# def random_destination() -> int:
#     return randint(11000, 11999)

# destination: int | None = Field(default_factory=random_destination)
# Here, Pydantic calls random_destination each time it creates a model instance without a destination. Two instances can still get the same number by chance.
# Pass the function without parentheses: default_factory=random_destination. Writing default_factory=random_destination() would call it immediately, like the first example.
