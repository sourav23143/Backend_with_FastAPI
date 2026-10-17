# BY DEFAULT, EACH ROUTE HAS THE 200 STATUS CODE FOR THE RESPONSE


from fastapi import FastAPI, HTTPException, status
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


#TO RAISE EXCEPTION THAT, GIVEN ID NOT FOUND

#FOR THAT WE HAVE TO IMPORT STATUS MODULE.AND THEN WE CAN USE IT HERE TO ACCESS ALL THE POSSIBLE STAUS CODES  
#status_code= status.HTTP_200_OK, by default it is HTTP_200_OK
#AND THAT WILL BE LIKE >

# @app.get("/shipment", status_code= status.HTTP_200_OK)


#BUT HERE WE WANT TO RAISE HTTP EXCEPTION (I.E EXCEPTION WHEN WORKING WITH FASTAPI), WHEN ID IS NOT FOUND 


#-----------------------------------------------------------------------------------------------------------------


# status_code sets the HTTP status returned when the route succeeds. Here, status.HTTP_200_OK means 200 OK: 
# the request worked and the response contains a shipment.

# For a valid ID, the function returns shipments[id] with status 200. If the ID isn’t in shipments, 
# your HTTPException raises 404 Not Found instead; that exception’s status overrides the decorator’s 
# success status.


# @app.get("/shipment", status_code= status.HTTP_200_OK) #by default staus code is 200_OK
#so we can write directly 
# @app.get("/shipment")


# @app.get("/shipment", status_code= status.HTTP_200_OK)
# def get_shipment(id: int | None = None) -> dict[str, Any]:
#     if id not in shipments:
#         raise HTTPException(
#             #inside it we will provide our status code as well as error details
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail = "Given id doesn't exist!"
#         )
#     return shipments[id]


# For a GET route, 200 is already the default, so you can write @app.get("/shipment") and get the same success status.
# status.HTTP_200_OK is a named constant for the number 200.


#-----------------------------------------------------------------------------------------------------------------


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            #inside it we will provide our status code as well as error details
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exist!"
        )
    return shipments[id]




@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )

