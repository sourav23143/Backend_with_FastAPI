
# ______________________________________________________________________________________

# HERE WE WILL CREATE A CONNECTION AND MANAGE A SESSION WITH OUR DATABASE

# AND INSTED OF MAKING A RAW CONNECTION WITH OUR SQLITE DATABASE, WE WILL GO AHEAD AND CREATE A SQLAlchemy ENGINE

# ______________________________________________________________________________________


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from typing import Annotated
from fastapi import Depends

from app.config import settings

engine = create_async_engine(
    url = settings.POSTGRES_URL, # URL of OUR DATABASE > here we not only have to provide file name of sqllite database but also the flavor,because we can use multiple flavour of sqlite databases, and because here we are using SQLite which is the dialect. so we have to provide it
    echo=True, # to get the SQL statements executed on our database , printed on the terminal as well
    
)






async def create_db_tables():
    async with engine.begin() as connection:
        from .models import Shipment

        await connection.run_sync(SQLModel.metadata.create_all(bind=engine)) #Create all tables stored in this metadata.




# # SESSION TO INTRACT WITH DATABASE
# async def get_session():
#     with AsyncSession(bind=engine) as session:  # creating a session with our database engine, and this session will be used to perform all the operations on our database
#         yield session  # yield the session so that it can be used in other parts of the application


# Insted of providing sesssion like this > it is recommended to wrap it in session maker  > to get some benifits


# SESSION TO INTRACT WITH DATABASE 
async def get_session():
    async_session = sessionmaker(
        bind=engine, #engine to bind with 
        class_=AsyncSession, ##by default class we use to create instance is async session , but in this case we have asyncsession, we will provide that 

        expire_on_commit=False # because we dont want to expire the connection with our database after we commit the changes, because we in some instance we refresh the databack as well after saving the changes

    )

    async with async_session() as session:
        yield session 

    # WE USE SESSION MAKER BECAUSE IT HAS BENIFITS LIKE CONNECTION POOLING, THREAD SHEFTY ALONG WITH OTHERS , SO THAT'S THE ONE EXTRA STEP WE HAVE DO WHEN USING ASYNCHRONOUS SESSION 




# SESSION DEPENDENCY ANNOTATION
SessionDep = Annotated[AsyncSession, Depends(get_session)]  # When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it


# When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it 
# and then provide values to our arguments 

# SO BY THESE WE HAVE MADE CONNECTION WITH OUR POSTGRES DATABASE AND ALSO HAVE THE SESSION DEPENDENCY THAT IS ASYNCHRONOUS AND WE CAN PROVIDE IT TO THE ENDPOINTS AS WELL  