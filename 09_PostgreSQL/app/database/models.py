from enum import Enum
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import EmailStr
from sqlmodel import Column, Field, SQLModel, Relationship # which we need to inherit to turn a normal Python class into a SQL model compatible with tables inside of our database
from sqlalchemy.dialects import postgresql 
from sqlalchemy import ARRAY, INTEGER

class ShipmentStatus(str, Enum): #str makes each enum member a string as well as an enum member.
    placed = "placed"
    transit = "in_transit"
    packed = "packed"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"



#______________________________________________________________________________________________

# BY THIS MODEL DEFINATION WE CAN GENERATE THE TABLE INSIDE OUR DATABASE 

#______________________________________________________________________________________________



class Shipment(SQLModel, table=True):
# By default sql model will use class name and convert it lowercase and then use it as our table name 

    # But we can go ahead and define custom one as well > 
    __tablename__ = "shipment"

    
    # id: int = Field(default=None, primary_key=True) # now because primary key is set to True and now if we not provide any id, it will automatically generate a unique id which will be like incrementing to new one
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4, 
            primary_key=True,)
            )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )

    
    content: str
    weight: float = Field(le=25, )
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime  #datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

    #seller_id: int = Field(foreign_key="seller.id") #foreign key which is realeated with seller
    seller_id: UUID = Field(foreign_key="seller.id")

    # if we dont have __tablename__, for defined model name, so by default it will be class name in lower case
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"})

    delivery_partner_id: UUID = Field(
        foreign_key="delivery_partner.id"
    )
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

# BENIFIT OF USING A MODEL LIKE THIS IS NOT TO JUST DEFINE THE TABLE, AS WELL AS USE THIS MODEL TO GET DATA OR SEND DATA TO THE DATABASE AS WELL
# I.E IF WE GET DATA BACK FROM OUR DATABASE SESSION, WE WILL GET IT AS AN INSTANCE OF THIS SHIPMENT CLASS


class User(SQLModel):
    name: str

    email: EmailStr
    password_hash: str = Field(exclude=True)









class Seller(User, table = True):

    __tablename__="seller"

    # by default table name will be class name only, so we have not added any table name
    # id: int = Field(default=None, primary_key=True)
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4, 
            primary_key=True,)
            )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )



    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# NOW WE HAVE ADDED THE SELLER TABLE TO OUR DATABASE, NOW WE CAN GO AHEAD AND RECIEVE THE DATA FOR A NEW SELLER IN THE ENDPOINT



class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4, 
            primary_key=True,)
            )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )


    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER)),
    )

    max_handling_capacity: int

    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )




    # METHOD TO FIND THE SHIPMENT THAT ARE ACTIVELY HANDLED BY THE DELIVERY PARTNER
    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
        ]

    # AMOUNT OF SHIPMENT DELIVERY PARTNER CAN HANDLE AT THE MOMENT
    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)



# A database model defines the structure and constraints of stored data. A
# database session is a temporary workspace used to query and modify that data.
#
# Key differences:
#
#   Aspect       Database Model                  Database Session
#   ------------ ------------------------------  ------------------------------
#   Purpose      Defines data structure.         Executes queries and transactions.
#   Lifetime     Persistent; evolves with       Temporary; lasts for a unit of
#                schema changes.                work or connection.
#   Scope        Describes database entities.   Holds state for one interaction.
#   Example      The Shipment SQLModel below.    A SQLAlchemy Session instance.
#
# In an ORM, model classes map fields to database tables. A session queries
# model instances, stages changes, and commits transactions. Closing a session
# releases its resources; uncommitted changes are generally rolled back.
                       