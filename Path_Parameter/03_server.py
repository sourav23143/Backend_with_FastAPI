#HOW FASTAPI WORK AND WHAT DECORATOR PLAY A ROLE ?

from typing import Callable, Any


routes: dict[str, Callable[[Any], Any]] = {} #Dict of  string(which will be path for the route), and this will have a function, which will be Callable Type


#route will be used as our decorator function and takes paths as argument for our decorator function
# and then we will create a inner function which will go ahead and register the route inside our route dictionary and return the function as is


def route(path: str):
    def register_route(func):
        routes[path] = func
        return func

    return register_route


@route("/shipment")
def get_shipment():
    return "<Shipment<1001, in transit>"

#so by this for path "/shipment" our function get_shipment() will be register in our routes dict.

#now to emulate the server, we will go ahead and create a request like this>
# and then create a while loop and run the same until request is quit


request: str = ""


while request != "quit":
    request = input(">   ")

    if request in routes:
        response = routes[request]()
        print(response, end = "\n\n")
    else:
        print("Not found")



# SO THIS IS GIVING US IDEA HOW ROUTING CAN BE HANDLE ROUTING LIKE THIS