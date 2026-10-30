import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any
from contextlib import contextmanager

#______________________________________________________________________________________________________________________

# NOW THAT WE HAVE LEARN HOW TO WORK WITH SQL DATABASES AND OPERATE ON SAME > NOW WE WILL USE THEM FOR OUR API ENDPOINT

# AND TO DO THAT, WE WILL CREATE A CLASS THAT WILL EXPOSE METHODS TO OPERATE WITH OUR DATABASE EASILY.

# I.E CREATE DATA POINTS, READ THEM AND UPDATE THE SAME AS WELL IN THE DATABASE MODULE

#______________________________________________________________________________________________________________________


class Database:


    def connect_to_db(self):
        # Make connection with database
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False) #path # and running database connection on diff thread > i,e we dont want to check same thread, but check another one
        # get cursor to execute queries and fetch data
        self.cur = self.conn.cursor() 
        print("connected to sqlite.db ....")


    #Create table if not exists
    def create_table(self):

        # 1. Create table with columns
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT
            )
        """)

    def create(self, shipment: ShipmentCreate) -> int:
        # Find as new id
        self.cur.execute("SELECT COALESCE(MAX(id), 0) FROM shipment")
        result = self.cur.fetchone()


        new_id = result[0] + 1
        #Insert values in the table

        # Insert values in the table
        self.cur.execute("""
            INSERT INTO shipment
            VALUES (:id, :content, :weight, :status)
        """, 
        {
            "id": new_id,
            **shipment.model_dump(),
            "status": "placed"
        }
        )

        # Commite the changes to the database
        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id = ?
        """, (id,))
        row = self.cur.fetchone() #if any id will be not present it will return None as well 


        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3],
        } if row else None


    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:

        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
            """,
            {
                "id": id, 
                **shipment.model_dump()
                
            }
        )
        self.conn.commit()

        return self.get(id)


    def delete(self, id: int):
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id = ?
        """, (id, ))
        self.conn.commit()




    def close(self):
        print("closed statement ....")
        self.conn.close()

    # def __enter__(self):
    #     print("enter the context")
    #     # when we enter inside of our context we can go and run some code
    #     # in this case will make some connection to database and create table as well 
    #     self.connect_to_db()
    #     self.create_table()
    #     return self  # returning database instance 


    # def __exit__(self, *arg):  # along with self we need to recieve other arguments as well that are positional > so we can recieve all of them using star operator and giving it a name which would be a list, and then we can go ahead and perform disposal of state if we want 
    #     print("existing the context")
    #     # in this case we want to exit out of our contex by closing the connection with the database
    #     self.close()


# CONTEX MANAGER Usage
# with Database() as db:
#     print(db.get(12701))
#     # here if we use db. sytax we will not get any suggestion for database method, because this need to be return from enter special method
#     print(db.get(12702))


# Here we have created database class ourselves, we can go ahead and these methods(def __enter___(), def __exit__()) in
# 
# But if we are importing the same from any other package or module we cant do that
# 
# so, Instead we go ahead and use a function approch. i.e we will define a function that does that for us, which will perform the setup and return us the value
# 
# Let's say database in this case, we will perform the same and when we exit out of the context, it does the same as well 


@contextmanager # it will make our function usuable with with statement
def managed_db():
    db = Database()
    # setup
    print("enter setup")
    db.connect_to_db()
    db.create_table()

    yield db

    print("exit the context")
    # Dispose
    db.close()




# for our function we cannot define enter or exit method, so we will insted decorate it with context manager, which will do it for us

with managed_db() as db:
    print(db.get(12701))
    print(db.get(12702))

