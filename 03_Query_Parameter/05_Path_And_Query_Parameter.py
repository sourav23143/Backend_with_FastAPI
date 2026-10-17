#  USING BOTH PATH AND QUERY PARAMETER TOGETEHR




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




@app.post("/shipment")
def submit_shipment(data: dict[str, Any]) -> dict[str, Any]:  # when we hint the arguments type as a dictionary. we aslo want to request data, because query parameter cannot be dictionary or anything like that 
    content = data["content"]
    weight = data["weight"]


    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = "Maximum weight limit is 25 kgs"
        )

    # Create and assign shipment a new id 
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed"
    }

    return {"id": new_id}

# SPECIFIC FIELD WHICH WILL BE PROVIDED IN THE REQUEST INSIDE OF THE SHIPMENT


# @app.get("/shipment/{field}") #field can be staus, content or the weight
# def get_shipment_field(field: str, id: int) -> dict[str, Any]: # id > query parameter
#     return {
#         field: shipments[id][field]
#     }

# IDEALY WE WILL ONLY HAVE GET SHIPMENT ENDPOINT, BUT THIS IS JUST DEMO FOR HOW WE CAN MIX AND MATCH THE QUERY AND PATH PARAMETERS

#INSTEAD OF RETURNING DICTIONARY WE CAN RETURN DIRECTLY FIELD VALUE LIKE THIS

@app.get("/shipment/{field}") #field can be staus, content or the weight
def get_shipment_field(field: str, id: int) -> Any: # id > query parameter
    return shipments[id][field]



@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )