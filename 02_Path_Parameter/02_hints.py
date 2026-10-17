#we can hints the type of function as well, which we recieve as arguments inside decorator function


#for hinting function type we use callable


from typing import Callable
from typing import Any


#and can take Callable as type of argument as function


# A Callable can take arguments which can more than one and also return something
# and we can hints on those types as well 

# def decorator(func: Callable[[int, int], float]):  #addition of two numbers
#     pass
 
def decorator(func: Callable[[Any], None]): #Callable[[Input Argument], Output]
    pass

