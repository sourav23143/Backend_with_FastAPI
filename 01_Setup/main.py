from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference 

app = FastAPI()




@app.get("/shipment") #here in its parameter we provide path for this route handler, when we want to handle this endpoint, we provide relative path here
def get_shipment():
    return {
        "content": "wooden table",
        "status": "in transit"
    }


# we can also have nested path like this >
#inside of seller, we only access shipment of that seller

# @app.get("/shipment")
# def get_shipment("/seller/shipment"):
#     return {
#         "content": "wooden table",
#         "status": "in transit"
#     }

#SO THATS HOW WE DEFINE THE API ENDPOINTS URL



#SO NOW OUR API ENDPOINTS ARE DEFINED

#NOW TO MAKE A REQUEST WE CAN WE CAN USE ANY BROWSER AS OUR API CLIENT


#BUT NOW IF WE HIT THIS URL, IT WILL GIVE NO RESPONSE BACK
#SINCE BECAUSE WE HAVE DEFINED OUR ENDPOINT HANDLER, BUT THERE IS NO SERVER RUNNING ACTUALLY TO ACCEPT THE
#REQUEST, PROCESS IT , AND SEND THE RESPONSE BACK

#SO FOR THAT WE HAVE TO START OUR FASTAPI SERVER

# fastapi dev > to start our server in dev mode


# CUSTOM DOCUMENTATION USING OPEN API SPECIFICATION
@app.get("/scalar", include_in_schema=False)
def get_return_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )
