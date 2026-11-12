# INSIDE THIS FILE WE WILL BRING ALL OF THE ROUTER INSIDE OUR API PACKAGE


from fastapi import APIRouter
from .routers import shipment, seller


# we will create a master router which will include all of the routers inside of  routers package, which we can include inside our main module 


master_router = APIRouter()

#on this master router we can include other router as well i.e any api router instance (i.e each router inside separate module)

master_router.include_router(shipment.router)
master_router.include_router(seller.router)