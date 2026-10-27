# NOW THAT WE HAVE LEARN HOW TO WORK WITH SQL DATABASES AND OPERATE ON SAME > NOW WE WILL USE THEM FOR OUR API ENDPOINT

# AND TO DO THAT, WE WILL CREATE A CLASS THAT WILL EXPOSE METHODS TO OPERATE WITH OUR DATABASE EASILY.

# I.E CREATE DATA POINTS, READ THEM AND UPDATE THE SAME AS WELL IN THE DATABASE MODULE





from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from .schemas import ShipmentStatus, ShipmentRead, ShipmentCreate, ShipmentUpdate
from .database import Database



app = FastAPI()


db = Database()


# TO LOAD JSON FILE WE WILL USE BUILT IN JSON MODULE TO LOAD AND SAVE THE JSON FILE
# database.py > TO HANDLE OUR JSON DATA





@app.get("/shipment", response_model = ShipmentRead) #hinting resonse model > WE USE IT WHEN WE ARE PROVIDING DIFFERENT TYPE, IN THIS CASE A LOOSELY TYPE DICTIONARY AND WE WANT TO IT VALIDATED AGAINST THIS SCHEMA
def get_shipment(id: int | None = None):
    # Check for shipment with given id 
    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(
            #inside it we will provide our status code as well as error details
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exist!"
        )
    return  shipment



@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:  

    new_id = db.create(shipment)
    # Return id for later use



    return {"id": new_id}





@app.patch("/shipment", response_model = ShipmentRead)
def patch_shipment(
    id: int, 
    shipment: ShipmentUpdate
    ) -> dict[str, Any]:

    # Update data with given fields
    shipment =  db.update(id, shipment)


    return shipment



@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}






@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    # return get_scalar_api_reference(
    #     openapi_url = app.openapi_url,
    #     title = "Scalar API" 
    # )
    return get_scalar_api_reference(
    openapi_url=app.openapi_url,
    title="Scalar API",
    scalar_js_url="https://cdn.jsdelivr.net/npm/@scalar/api-reference@1.72.0",
)
