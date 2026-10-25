# DIFFERENT SCHEMA FOR DIFFRENT USE CASES>






from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from .schemas import ShipmentStatus, ShipmentRead, ShipmentCreate, ShipmentUpdate
from .database import save, shipments



app = FastAPI()



# TO LOAD JSON FILE WE WILL USE BUILT IN JSON MODULE TO LOAD AND SAVE THE JSON FILE
# database.py > TO HANDLE OUR JSON DATA





@app.get("/shipment", response_model = ShipmentRead) #hinting resonse model > WE USE IT WHEN WE ARE PROVIDING DIFFERENT TYPE, IN THIS CASE A LOOSELY TYPE DICTIONARY AND WE WANT TO IT VALIDATED AGAINST THIS SCHEMA
def get_shipment(id: int | None = None):
    if id not in shipments:
        raise HTTPException(
            #inside it we will provide our status code as well as error details
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exist!"
        )
    return  shipments[id]



@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:  

    # Create and assign shipment a new id 
    new_id = max(shipments.keys()) + 1

    # shipments[new_id] = {
    #     "content": shipment.content,
    #     "weight":shipment.weight,
    #     "destination": shipment.destination,
    #     "status": "placed"
    # }

    #we can also convert our Schema  Pydantic Model  into dict as well, using model_dump method on our shipment
    # shipment.model_dump() #Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
    # so we will simply unpack it inside our dictionary

    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed"
    }
    save()


    return {"id": new_id}





@app.patch("/shipment", response_model = ShipmentRead)
def patch_shipment(
    id: int, 
    body: ShipmentUpdate
    ) -> dict[str, Any]:

    shipment = shipments[id]
    # Update the provided filds
    # instead of picking each field one by one , we can take our shipment which is a dict and upadte it with another dictionary using the update method

    shipment.update(body.model_dump(exclude_none=True)) #D.update([E, ]**F) -> None. Update D from mapping/iterable E and F.
    shipments[id] = shipment
    save()
    return shipment[id]



@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
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
