import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

#______________________________________________________________________________________________________________________


#______________________________________________________________________________________________________________________


class Database:
    def __init__(self):  #i.e when we initialize our instance we'll go ahead and make a connection with our database
    
        #database connection
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False) #path # and running database connection on diff thread > i,e we dont want to check same thread, but check another one
        # get cursor to execute queries and fetch data
        self.cur = self.conn.cursor() # using our cursor we can execute sql language i.e our query
        # Create table if not exists
        self.create_table()

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
        self.conn.close()
    