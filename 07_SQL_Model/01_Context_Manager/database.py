import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

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

    def __enter__(self):
        print("enter the context")
        # when we enter inside of our context we can go and run some code
        # in this case will make some connection to database and create table as well 
        self.connect_to_db()
        self.create_table()
        return self  # returning database instance 


    def __exit__(self, *arg):  # along with self we need to recieve other arguments as well that are positional > so we can recieve all of them using star operator and giving it a name which would be a list, and then we can go ahead and perform disposal of state if we want 
        print("existing the context")
        # in this case we want to exit out of our contex by closing the connection with the database
        self.close()









   
# Usage
# db = Database() 

# db.get(12701)
# db.get(12702)

# db.close()

# WE ALWAYS HAVE TO REPEAT THESE TWO STEPS WHENEVER WE WANT TO MAKE ANY OPERATION ON THE DATABASE
# I.E 
# TO INITILIZED THE SAME TO MAKE A CONNECTION TO THE DATABASE, PERFORM THE ACTIONS AND THEN CLOSE

#_____________________________________________________________________________________________

# INSTED WE AUTOMATICALLY MANAGED FOR US USING CONTEX MANAGERS > 
# I.E OUR DATABASE WILL BE OUR CONTEX AND FOR MANAGING WE GO AHEAD AND MANAGE OUR CONNECTION
# I.E IT'S OPENING (THAT IS MAKING A CONNECTION) WHEN WE START AND WHEN WE ARE DONE WE WILL CLOSE THAT AS WELL

# IT IS SOMETHING SIMILAR TO HOW WE USE FILE IN PYTHON
# I.E WE USE "with" statement do define a contex manager and open the file with provide the path, and then alias the return type
# and then we can go ahead and operate on the same > i.e read its content >  and we are done  we simply exit with with block by intenting out of the same 

# CONTEX MANAGER Usage
# with Database() as db:
#     print(db.get(12701))
#     # here if we use db. sytax we will not get any suggestion for database method, because this need to be return from enter special method
#     print(db.get(12702))




# NOW IF WE RUN THIS PROGRAM BY > 

# python .\app\database.py
# 
# we will get module not found error, as we have also imported app package i.e from the app package we have imported schema, which it cannot resolve
# because we have to provide app in the contex as well 

# python -m app.database

# we have used "-m", to skip the .py 