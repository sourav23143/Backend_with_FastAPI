from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()





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


#QUERY PARAMETER

# @app.get("/shipment")
# def get_shipment(id: int) -> dict[str, Any]:
#     if id not in shipments:
#         return {"details": "Given id doesn't exist!"}
#     return shipments[id]


#QUERY PARAMETER>
# http://127.0.0.1:8000/shipment?id=12702  >

# {
#   "id": 12702,
#   "content": "wooden table",
#   "weight": 1.2,
#   "status": "in transit"
# }


#IMP > JUST LIKE PATH PARAMETER, QUERY PARAMETERS HAVE VALIADTION AND OTHER THING AS WELL 
#I.E IF WE PASS STRING/FLOAT VALUE WE WILL GET ERROR

#IF WE DONT PASS ID QUERY PARAMTER IN OUR REQUEST THAN WE WILL GET AN ERROR > ID QUERY PARAMETER IS MISSING

# SO WE CAN MAKE IT OPTIONAL AS WELL, BY USING TYPE HINT


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]
    if id not in shipments:
        return {"details": "Given id doesn't exist!"}
    return shipments[id]

# not id asks whether id is false-like, such as None, 0, or "".
# id not in shipments asks whether id is not a key in the shipments dictionary.


@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )




