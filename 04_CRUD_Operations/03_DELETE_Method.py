 
# ENDPOINT TO UPDATE THE EXISTING DATA

# i.e Fields of existing shipment


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
def submit_shipment(data: dict[str, Any]) -> dict[str, Any]:  # when we hint the argumens type as a dictionary. we aslo want to request data, because query parameter cannot be dictionary or anything like that 
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




@app.put("/shipment")
def shipment_update(id: int, content: str, weight: float, staus: str) -> dict[str, Any]:
    shipments[id] = {   
        "content": content,
        "weight": weight,
        "status": staus,
    }
    return shipments[id]

#---------------------------------------------------------------------------------------------------------------------------------------


# FOR OUR SHIPMENT, WE PROBABLY WON'T CHANGE THE CONTENT AND THE WEIGHT AFTER IT IS FINALIZED 
# WE WILL ONLY CHANGE THE STATUS FOR TRACKING

#SO HERE INSTED OF USING PUT METHOD TO REMOVE THE EXISTING DATA AND REPLACE IT WITH THE DATA PROVIDED
# WE WILL ONLY CHANGE ONE FILED OR A FEW FIELD USING ANOTHER METHOD CALLED "PATCH" 
# AS PUT METHOD IS USED FOR FULL REPLACEMENT OF FILED THOSE ARE DEFINED , IF WE LEFT ANY ONE OF THOSE FILED, IT WILL GIVE ERROR

#-----------------------------------------------------------------------------------------------------------------------------------------

# @app.patch("/shipment")
# def patch_shipment(
#     id: int, 
#     content: str | None = None , 
#     weight: float | None = None, 
#     status: str | None = None
#     ):

#     shipment = shipments[id]
#     # Update the provided filds
#     if content:
#         shipment["content"] = content
#     if weight:
#         shipment["weight"] = weight
#     if status:
#         shipment["status"] = status

#     shipments[id] = shipment
#     return shipment

# THESE ID, CONTENT, WEIGHT, STATUS ARE ULTIMETLY QUERY PARAMETER, SO WE CAN ALSO PASS THEM WITHIN THE URL 

# ONLY DRAWBACK RIGHT NOW, IS WHEN WE TRY TO UPDATE THE FILED, IF THEY ARE PROVIDED, WE USE THE IF STATEMENTS AND DO THAT FOR EACH FILEDS
# AND IF WE HAVE MORE FILDS, THEN WE NEED TO DO IT AGAIN AND AGAIN. SO, INSTED WE CAN RECIEVE THE DATA AS UPADTE DATA AS A REQUEST BODY



@app.patch("/shipment")
def patch_shipment(
    id: int, 
    body: dict[str, Any]
    ):

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
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API" 
    )