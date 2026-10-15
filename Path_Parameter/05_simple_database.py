from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()


#TILL NOW WE HAVE USED HARD CODED DATA INSIDE OUR ROUTES
#LET SAY INSTED WE HAVE SOME SHIPMENTS AND FROM THAT WE WILL GET THE SHIPMENT BASED ON "ID" PROVIDED OR GET THE LATEST ONE FROM THE SAME 


shipments = {
    12701: {
        "id": 12701,
        "content": "glassware",
        "weight": .6,
        "status":  "palced"
    },
    12702: {
        "id": 12702,
        "content": "wooden table",
        "weight": 1.2,
        "status": "in transit"
    },
    12703: {
        "id": 12703,
        "content": "electronics",
        "weight": 2.4,
        "status": "packed"
    },
    12704: {
        "id": 12704,
        "content": "textiles",
        "weight": 3.1,
        "status": "delivered"
    },
    12705: {
        "id": 12705,
        "content": "ceramics",
        "weight": 0.9,
        "status": "in transit"
    },
    12706: {
        "id": 12706,
        "content": "machinery",
        "weight": 5.7,
        "status": "packed"
    },
    12707: {
        "id": 12707,
        "content": "furniture",
        "weight": 4.6,
        "status": "delivered"
    }
}

#now we have our shipments data and now we can use it inside our route functions


#IF WE PASS ANY ID TO OUR ROUTE WHICH IS NOT PRESENT THEN IT WILL GIVE US INTERNAL SERVER ERROR, SO FOR THIS WE HAVE TO DO ERROR HANDLING
#I.E IF ID IS NOT PRESENT INSIDE THE DICTIONARY WE NEED TO RETURN SOME MESSAGES I.E "GIVEN ID DOES NOT EXIST"

#latest 
@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


#IF WE PASS ANY ID TO OUR ROUTE WHICH IS NOT PRESENT THEN IT WILL GIVE US INTERNAL SERVER ERROR, SO FOR THIS WE HAVE TO DO ERROR HANDLING
#I.E IF ID IS NOT PRESENT INSIDE THE DICTIONARY WE NEED TO RETURN SOME MESSAGES I.E "GIVEN ID DOES NOT EXIST"



# /shipment/12701  > 1270 will be caught by fastapi and provided to same inside our router function
@app.get("/shipment/{id}")
def get_shipment(id: int | float) -> dict[str, Any]:
    if id not in shipments:
        return {"details": "Given id doesn't exist!"}
    return shipments[id]




# CUSTOM DOCUMENTATION USING OPEN API SPECIFICATION
@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )

