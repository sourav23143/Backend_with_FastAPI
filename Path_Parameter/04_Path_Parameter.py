from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()


#Latest shipment
#order also matter as if "/shipment/{id}" will be first it will ctach the /shipment/latest request and give error by integer valiadtion in path parameter

#SO THATS WHY ORDER OF THESE ROUTES MATTER WHEN WE HAVE POSITIONAL PARAMETERS AND SOME SET VALUES LIEK THESE
@app.get("/shipment/latest")
def get_latest_shipment():

    return {
        "id": 12798,
        "content": "glassware",
        "weight": .6,
        "status":  "palced"
    }




# /shipment/12701  > 1270 will be caught by fastapi and provided to same inside our router function
@app.get("/shipment/{id}")
def get_shipment(id: int | float) -> dict[str, Any]:
#def get_shipment(id: int | float) -> dict[str, str | int | float]:

    return {
        "id": id,
        "content": "wooden table",
        "weight": 1.2,
        "status":  "in transit"
    }


#now if we provide it something instead of integer,  like string "latest", it will catch that as well
#now if we want to make it something like we not want only integer, then for that we have to type hint the path parameter, when we recieve it inside our function

#and now fastapi will handle valiadtion for us and now if we pass http://127.0.0.1:8000/shipment/latest we will get error as >


# {
#   "detail": [
#     {
#       "type": "int_parsing",
#       "loc": [
#         "path",
#         "id"
#       ],
#       "msg": "Input should be a valid integer, unable to parse string as an integer",
#       "input": "latest"
#     }
#   ]
# }


#---------------------------------------------------------------------------------------------------------------------------------

#Latest shipment


@app.get("/shipment/latest")
def get_latest_shipment():

    return {
        "id": 12798,
        "content": "glassware",
        "weight": .6,
        "status":  "palced"
    }






# CUSTOM DOCUMENTATION USING OPEN API SPECIFICATION
@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )

