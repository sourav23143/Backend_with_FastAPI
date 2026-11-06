
# ______________________________________________________________________________________

# HERE WE WILL CREATE A CONNECTION AND MANAGE A SESSION WITH OUR DATABASE

# AND INSTED OF MAKING A RAW CONNECTION WITH OUR SQLITE DATABASE, WE WILL GO AHEAD AND CREATE A SQLAlchemy ENGINE

# ______________________________________________________________________________________


from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from typing import Annotated
from fastapi import Depends



engine = create_engine(
    url = "sqlite:///sqlite.db", # URL of OUR DATABASE > here we not only have to provide file name of sqllite database but also the flavor,because we can use multiple flavour of sqlite databases, and because here we are using SQLite which is the dialect. so we have to provide it
    echo=True, # to get the SQL statements executed on our database , printed on the terminal as well
    connect_args={"check_same_thread": False},
)






def create_db_tables():
    from .models import Shipment

    SQLModel.metadata.create_all(bind=engine) #Create all tables stored in this metadata.


# session = Session(engine) # creating a session with our database engine, and this session will be used to perform all the operations on our database
# session.get(
#     Shipment,
#     12701
# )  #Return an instance based on the given primary key identifier, or None if not found.


# # INSTED OF TUPLE OF VALUES, WE GET A SHIPMENT OBJECT BACK I.E A SHIPMENT OBJECT ON WHICH WE CAN ACCESS ALL THE FILEDS AND SO ON

# # LET SAY WE WANT TO ADD DATA TO OUR DATABASE 
# # SO FOR IT WE WILL USE ADD SESSION AND THEN WE CAN USE ADD METHOD AND THEN WE WILL PROVIDE INSTANCE OF DATA WE WANT TO ADD 
# session.add(
#     Shipment(id=12701, content="Books", weight=10.5, destination=12345, status="placed")
#     # we can skip id even if as we in our SQL Model Session defination we have set "id" as primary key and default to None, because it will automatically generate a unique id for us, but here we are providing it manually
# )

# # AND ONCE WE HAVE MADE CHANGES TO OUR DATABASE SESSION WE CAN COMMIT THOSE SESSION AS
# session.commit()

#________________________________________________________________________________________________________________________________________

# RETURN NEW SESSION >
def get_session():
    with Session(bind=engine) as session:  # creating a session with our database engine, and this session will be used to perform all the operations on our database
        yield session  # yield the session so that it can be used in other parts of the application

# NOW WE CAN PASS THIS SESSION IN MAIN.PY ENDPOINTS AND USE IT TO PERFORM OPERATIONS ON OUR DATABASE, I.E CREATE, READ, UPDATE AND DELETE DATA POINTS IN OUR DATABASE

# AND BECAUSE OUR SESSION HAS A CONTEXT MANAGER, WE CAN GO AHEAD AND WRAP IT IN WITH STATEMENT AS WELL 




SessionDep = Annotated[Session, Depends(get_session)]  # When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it


# When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it 
# and then provide values to our arguments 
