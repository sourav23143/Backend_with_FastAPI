import json # handle load and save

shipments = {}

#loading our file > json load method 
with open("shipments.json") as json_file: #by default it is open in reading mode
    data = json.load(json_file) # we will get all databack, which will be list of datapoints

    for value in data:
        shipments[value["id"]] = value

print(shipments)

# ONCE WE HAVE THE DATA LOADED IN THE FORM OF JSON FILE, WE ALSO HAVE TO SAVE THE CHANGES MADE TO OUR SHIPMENTS, I.e IN OUR ENDPOINT WHEN WE CREATE A NEW SHIPMENT, WE HAVE TO SAVE THAT CHANGE
# AND WHEN WE UPDATE THE FILEDS OF EXISTING SHIPMENT WE HAVE TO SAVE THOSE CHANGES AS WELL 


#SAVE FUNCTION > WHICH WILL TAKE CHANGES AND PUT IT INSIDE OF THE shipments.json file 

def save():
    with open("shipments.json", 'w') as json_file:
        json.dump(
            list(shipments.values())   #Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object).
        )

