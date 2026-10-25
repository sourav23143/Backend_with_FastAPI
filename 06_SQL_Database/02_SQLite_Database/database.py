import sqlite3



#database connection
connection = sqlite3.connect("sqlite.db") #path
#with connection we can perform all the action we want



#once we have connection, we have to go ahead and get a cursor to edit our file.(i.e our database)
cursor = connection.cursor() # using our cursor we can execute sql language i.e our query


# 1. Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipment (
    id INTEGER PRIMARY KEY,
    content TEXT,
    weight REAL,
    status TEXT
    )
""")


# AFTER SETTING IT PRIMARY KEY, IF WE TRY TO CREATE DUBLICATE DATA > WE WILL GET A ERROR 

# cursor.execute("DROP TABLE shipment")
# connection.commit() #it can be done without commiting as well, since it a table operation


# 2. Add shipment data
# cursor.execute("""
#     INSERT INTO shipment
#     VALUES (12701, 'metal gears', 12, 'placed')
# """)

# #we will not able to see it as now we have made changes to database, we have to save that as well i.e commit the changes 
# connection.commit() #push the changes to database 


#database have blogs insted of simple text, so can use extension to open our sql lite file > 

#_________________________________________________________________________________________________________________________________

#-------------------------------------------------------------------------------------------------------

# # 3. Reading a shipment by id >
# cursor.execute("""
#     SELECT * FROM shipment
# """)

# # by this we will not get databack > so for fetching we have to featch data
# # result = cursor.fetchall()
# # print(result)

# #[(12701, 'palm trees', 8.5, 'placed'), (12702, 'basalt', 18.7, 'in_transit')]

# #-------------------------------------------------------------------------------------------------------
# #if we want we can limit the data that being selected > for that use fetchmany() method and provided the no. of rows we want

# # result = cursor.fetchmany(2) #only fetch two results > select statement fetch all the statement as per the query, but when we fetch we limited to two result
# # print(result)


# # [(12701, 'palm trees', 8.5, 'placed'), (12702, 'basalt', 18.7, 'in_transit')]

# #-------------------------------------------------------------------------------------------------------
# result = cursor.fetchone() # if we wnat to fetch one result only
# print(result)

# #(12701, 'palm trees', 8.5, 'placed')

#_________________________________________________________________________________________________________________________________




# 3. Reading a shipment by id >
# cursor.execute("""
#      SELECT * FROM shipment 
#      WHERE id = 12702
#  """)

# cursor.execute("""
#     SELECT status FROM shipment
#     WHERE content = 'palm trees'
# """
#     )


# result = cursor.fetchone()
# print(result)


# _________________________________________________________________________________________________________________________________

# 4. Update a shipment 

cursor.execute("""
    UPDATE shipment SET status = 'in_transit'
    WHERE id = 12701
""")

connection.commit()







# _________________________________________________________________________________________________________________________________

# 5. Delete a shipment by id
cursor.execute("""
    DELETE FROM shipment
    WHERE id = 12703
""")


connection.commit() #since here we have change something, so we have commit 





















# close the connection when done
connection.close()
