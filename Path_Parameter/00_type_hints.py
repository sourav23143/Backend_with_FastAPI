text = "value"

#python interpreater will assign it type at run time, in this case, we will assign it type (string)

#now since, it is dynamic in nature we can, later on change its type like this as well >

text = 0 #and it is totally valid

#--------------------------------------------------------------------------------------------------

#insted we can hint on data type 
text: str = "value"


#now we are only hinting on type but we are not strictly typing it , means previous expression is still valid and we can change it to float
#and it will not raise any error
text = 10.0

#But we can use tools like Mypy to give error messages

pert: int = 90
temp: float = 37.5


#another type >
#file: bytes = FileData()


#--------------------------------------------------------------------------------------------------
#by default we get type hint and suggestion in our code editors
#like this >
#if we assign a variable as string value as >
# value = "string"
# value.capitalize #our editor will give suggestion on the methods available for string type


#BUT SAME DOESNOT WORK INSIDE OF THE FUNCTION >

# def root(num):
#     num.  #now this will not give any suggestion as datatype can be dynamic in nature 
#     return pow(num, .5)


#but if we will type hint it we will get suggestion> 

# def root(num: int):
#     num.as_integer_ratio() #now we will get all the method of type int class
#     return pow(num, .5)


# root_25 = root(25)
# root_25.  #now not get any sugesstion

# root_25: float = root(25)
# root_25.as_integer_ratio #now will get all the methods of float type


# BUT BETTER WAY TO DO THIS IS TO HINT RETURN TYPE OF THE FUNCTION INSTED OF LIKE THIS

# def root(num: int) -> float:
#     return pow(num, .5)

# root_25 = root(25)
# root_25.as_integer_ratio() #method of float



#--------------------------------------------------------------------------------------------------

#WHEN WE HAVE TO DEFINE A NUMBER WHICH CAN BE OF TWO TYPES, THEN FOR THAT WE USE PIPE OPERATOR "|"

number: int | float = 12

#now we can use same inside root function as well 

def root(num: int | float) -> float:
    return pow(num, .5)

root_25 = root("25") 
# #to get warning, when we use different type of value then expected, we can use Mypy extension


#--------------------------------------------------------------------------------------------------
#Using same pipe operator we can make a value optional as well 

optional: str | None

optional  = "value"

#can use same thing in our function as well 

# def root(num: int | float, exp: float | None):
#     return pow(num, .5 if exp is None else exp)



# OR BETTER WE CAN PROVIDE IT A DEFAULT VALUE IN FUNCTION DEFINATION AS ITSELF AS >

# def root(num: int | float, exp: float | None = .5):
#     return pow(num, exp)

#--------------------------------------------------------------------------------------------------
# we can hint on sequence data type as well

digits: list[int] = [1, 2, 3, 4, 5]

table_5: tuple[int, ...] = (5, 10, 15, 20, 25)  # ... > to say tuple that it contains multiple elements

city_temp: tuple[str, float] = ("City", "20.5") #here we are hinting that length of tuple is "2" and datatype of each element


shipment: dict[str, str | int] = {
    "id": 12701,
    "content": "wooden table",
    "status": "in transit",

}

from typing import Any
shipment: dict[str, Any] = {
    "id": 12701,
    "weight": 1.2,
    "content": "wooden table",
    "status": "in transit",

}
#--------------------------------------------------------------------------------------------------


# WE CAN USE CUSTOM CLASSES AS TYPE HINT AS WELL >

class City:
    def __int__(self, name, location):
        self.name = name,
        self.location = location

hampshire = City("hampshire", 20364685)
city_temp: tuple[City, float] = (hampshire,  20.5)
