
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()





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



#--------------------------------------------------------------------------------------------------------------------------

@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, int]:  #recieving the shipment data as query parameter
    
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Maximum weight limit is 25 kgs"
        )
    
    
    
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed"
    }

    return {"id": new_id}

# creating a new endpoint which will recieve new shipment data from the client in the server


# CLIENT POST NEW SHIPMENT DATA LET SAY, WEIGHT AND CONTENT 
# WE RECIEVE IT IN OUR HANDLER FUNCTION CREATE A NEW ENTITY, WHICH WOULD BE OUR SHIPMENT, AND THEN RETURN BACK ITS ID

@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )