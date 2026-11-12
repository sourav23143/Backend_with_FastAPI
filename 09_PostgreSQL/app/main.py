# NOW THAT WE HAVE LEARN HOW TO WORK WITH SQL DATABASES AND OPERATE ON SAME > NOW WE WILL USE THEM FOR OUR API ENDPOINT

# AND TO DO THAT, WE WILL CREATE A CLASS THAT WILL EXPOSE METHODS TO OPERATE WITH OUR DATABASE EASILY.

# I.E CREATE DATA POINTS, READ THEM AND UPDATE THE SAME AS WELL IN THE DATABASE MODULE





from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

# from .database import Database
from app.api.router import master_router           #we can include master router inside our app, to include all of the app define inside our API
from app.database.session import create_db_tables

# we can use our lifespan handler to create our database table 
# i.e inside of our lifespan handler we will create database table 

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables() # calling the function to create database tables when the server is started
    yield
    print("...stopped!")




app = FastAPI(lifespan=lifespan_handler)



app.include_router(master_router)

#db = Database()


# TO LOAD JSON FILE WE WILL USE BUILT IN JSON MODULE TO LOAD AND SAVE THE JSON FILE
# database.py > TO HANDLE OUR JSON DATA


# endpoint to create a new seller
@app.post("/seller/signup")
def register_seller(seller):
    pass 





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
