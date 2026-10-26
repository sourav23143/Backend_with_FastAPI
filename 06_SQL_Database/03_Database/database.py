import sqlite3
from schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

#______________________________________________________________________________________________________________________

# NOW THAT WE HAVE LEARN HOW TO WORK WITH SQL DATABASES AND OPERATE ON SAME > NOW WE WILL USE THEM FOR OUR API ENDPOINT

# AND TO DO THAT, WE WILL CREATE A CLASS THAT WILL EXPOSE METHODS TO OPERATE WITH OUR DATABASE EASILY.

# I.E CREATE DATA POINTS, READ THEM AND UPDATE THE SAME AS WELL IN THE DATABASE MODULE

#______________________________________________________________________________________________________________________


class Database:
    def __init__(self):  #i.e when we initialize our instance we'll go ahead and make a connection with our database
    
        #database connection
        self.conn = sqlite3.connect("sqlite.db") #path
        # get cursor to execute queries and fetch data
        self.cur = self.conn.cursor() # using our cursor we can execute sql language i.e our query
        # Create table if not exists
        self.create_table("shipment")

    #Create table if not exists
    def create_table(self, name: str):

        # 1. Create table with columns
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS ? (
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT
            )
        """, (name,))

    def create(self, shipment: ShipmentCreate) -> int:
        # Find as new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
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


    def update(self, shipment: ShipmentUpdate) -> dict[str, Any]:

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
        self.conn.close()
    