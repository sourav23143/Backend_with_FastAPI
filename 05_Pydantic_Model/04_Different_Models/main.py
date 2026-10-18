# DIFFERENT SCHEMA FOR DIFFRENT USE CASES>






from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from .schemas import Shipment, ShipmentStatus

app = FastAPI()







shipments = {
    12701: {
        "content": "glassware",
        "weight": 2.6,
        "destination": 124773,
        "status":  "placed"
    },
    12702: {
        "content": "wooden table",
        "weight": 1.2,
        "destination": 124774,
        "status": "in_transit"
    },
    12703: {
        "content": "electronics",
        "weight": 2.4,
        "destination": 124775,
        "status": "packed"
    },
    12704: {
        "content": "textiles",
        "weight": 3.1,
        "destination": 124776,
        "status": "delivered"
    },
    12705: {
        "content": "ceramics",
        "weight": 10.9,
        "destination": 124777,
        "status": "in_transit"
    },
    12706: {
        "content": "machinery",
        "weight": 5.7,
        "destination": 124778,
        "status": "packed"
    },
    12707: {
        "content": "furniture",
        "weight": 4.6,
        "destination": 124779,
        "status": "delivered"
    }
}



@app.get("/shipment", response_model = Shipment) #hinting resonse model > WE USE IT WHEN WE ARE PROVIDING DIFFERENT TYPE, IN THIS CASE A LOOSELY TYPE DICTIONARY AND WE WANT TO IT VALIDATED AGAINST THIS SCHEMA
def get_shipment(id: int | None = None):
    if id not in shipments:
        raise HTTPException(
            #inside it we will provide our status code as well as error details
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exist!"
        )
    return  shipments[id]



@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:  

    # Create and assign shipment a new id 
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": shipment.content,
        "weight":shipment.weight,
        "status": "placed"
    }

    return {"id": new_id}








@app.put("/shipment")
def shipment_update(id: int, content: str, weight: float, staus: str) -> dict[str, Any]:
    shipments[id] = {   
        "content": content,
        "weight": weight,
        "status": staus,
    }
    return shipments[id]


@app.patch("/shipment")
def patch_shipment(
    id: int, 
    body: dict[str, ShipmentStatus]
    ) -> dict[str, Any]:

    shipment = shipments[id]
    # Update the provided filds
    # instead of picking each field one by one , we can take our shipment which is a dict and upadte it with another dictionary using the update method

    shipment.update(body) #D.update([E, ]**F) -> None. Update D from mapping/iterable E and F.

    shipments[id] = shipment
    return shipment



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
