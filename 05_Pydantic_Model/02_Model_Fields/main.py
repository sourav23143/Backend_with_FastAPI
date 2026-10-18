


from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from enum import Enum

from .schemas import Shipment

app = FastAPI()



#now we have class that we want to use it inside for data validation for request body data,
#  And to do that we can inherit the Pydantic base model in this class to make it API schema
# i.e get all data valiadtions for the fields

# Now to use this in our endpoint, we can go ahead and simply hint on the type that is will get the request body insted of dictionary type


    



shipments = {
    12701: {
        "content": "glassware",
        "weight": .6,
        "status":  "palced"
    },
    12702: {
        "content": "wooden table",
        "weight": 1.2,
        "status": "in transit"
    },
    12703: {
        "content": "electronics",
        "weight": 2.4,
        "status": "packed"
    },
    12704: {
        "content": "textiles",
        "weight": 3.1,
        "status": "delivered"
    },
    12705: {
        "content": "ceramics",
        "weight": 0.9,
        "status": "in transit"
    },
    12706: {
        "content": "machinery",
        "weight": 5.7,
        "status": "packed"
    },
    12707: {
        "content": "furniture",
        "weight": 4.6,
        "status": "delivered"
    }
}


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            #inside it we will provide our status code as well as error details
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exist!"
        )
    return shipments[id]

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



#_________________________________________________________________________________________________________
#Enum 

class ShipmentStatus(str, Enum):
    placed = "placed"
    transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"






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