



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

# WHEN WE USE THE POST METHOD, WE RECIEVE DATA FROM THE CLIENT, AND HERE WE'RE DOING THE SAME
#EX > 

# /shipment?content=value&weight=20&key=value


#--------------------------------------------------------------------------------------------------------------------

# AS A CLINT WE CAN SEND REQUEST OTHER WAY AS WELL, I.E BY REQUEST BODY


#INSIDE OUR REQUEST BODY WE CAN PROVIDE THE DATA AS JSON OR ANY OTHER FORMAT AS WELL 
#BUT HERE WE WILL USE JSON, BECAUSE THAT IS WHAT WE ARE RETURNING FROM THE SERVER AS WELL 

# THAT'S THE DIFFRECE B/W GET METHOD AND POST METHOD 

# IN GET METHOD WE GET DATA FROM THE SEVER SO IT DOESNOT HAVE BODY PARAMTER, AND IN POST METHOD WE ALREADY HAVE THOSE TO 
# PROVIDE A BODY FOR OUR REQUEST 


#WE CAN PROVIDE DATA IN JSON AS SOME DICTIONARY AS LIKE > 
# {
#     "key": 100
# }

# IF WE SEND THE REQUEST IT WILL SEND THE REQUEST AND ALSO INCLUDE THE REQUEST BODY
#TO PREVIEW THE SAME WE WILL ALSO HAVE TO ACCEPT THE SAME INSIDE OUR ROUTE HANDLER AS WELL
#SO FOR IT JUST LIKE OUR QUERY PARAMETERS WE WILL GO AHEAD AND RECIEVE IT AS A ARGUMENT 


# @app.post("/shipment")
# def submit_shipment(data: dict[str, Any]) -> dict[str, Any]:  # when we hint the argumens type as a dictionary. we aslo want to request data, because query parameter cannot be dictionary or anything like that 
#     content = data["content"]
#     weight = data["weight"]


#     if weight > 25:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail = "Maximum weight limit is 25 kgs"
#         )

#     # Create and assign shipment a new id 
#     new_id = max(shipments.keys()) + 1

#     shipments[new_id] = {
#         "content": content,
#         "weight": weight,
#         "status": "placed"
#     }

#     return {"id": new_id}



#----------------------------------------------------------------------------------------------------------------------

# if we want to recieve query parameter along with body we can aslp do that 

# recieving weight as query parameter


@app.post("/shipment")
def submit_shipment(weight: float, data: dict[str, str]) -> dict[str, Any]:  
    content = data["content"]
    

    # Validating weight
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

#  SO THAT'S HOW WE CAN MATCH AND MIX QUERY PARAMETER AND REQUEST BODY TOGETHER, BUT IT MAKE MORE SENSE TO JUST ASS THIS INSIDE OF REQUEST BODY ALL TOGETHER



@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )