import time
from rich import print
import asyncio

async def endpoint(route: str) -> str:
    print(f">> handling `{route}` endpoint...")

    # emulate database delay
    await asyncio.sleep(1) # because our sleep function is synchronous we have to use a asynchronous equivalent as well, that will be comming from asyncio, and we also have to await this to run this beacause this gives us a coroutine

    print(f"<< response from `{route}` endpoint!")
    return route


# TO MAKE OUR CODE ASYNCHRONOUS WE HAVE TO ADD ASYNC KEYWORD BEFORE THE FUNCTION DEFINATION 
# THIS DOES TWO THINGS >

# I.E MAKE OUR FUNCTION ASYNCHRONOUS AND ADD THE CAPABILITY TO RUN ANY ASYNCHRONOUS CODE INSIDE ITS FUNCTION BLOCK 
# AND MAKES THIS FUNCTION A "COROUTINE" (WHICH IN SHORT IS FOR ASYNCHRONOUS FUNCTION IN PYTHON )

#________________________________________________________________________
# A coroutine is a program component that can pause its execution, 
# yield control, and later resume from the exact point it left off
#________________________________________________________________________

# endpoint("")  #(function) def endpoint(route: str) -> CoroutineType[Any, Any, str]
# WE GOT HERE A COROUTINE, WHEN WE RUN THIS COROUTINE OUR ASYNCHRONOUS FUNCTION THEN WE WILL GET OUR RESULT BACK WHICH WOULD BE OF TYPE STRING

# A COROUTINE IS AN ASYNCHRONUS CODE IN PYTHON AND WHEN WE ACTUALLY CALL THE SAME. I.E BRACES ON THE FUNCTION IT DOES NOT RUN THIS 
# CODE INSIDE, INSTEAD IT ONLY PROVIDE US A COROUTINE
# AND WE HAVE TO RUN THIS COROUTINE IN TURN TO GET THIS RESULT BACK (I,E RUN THIS CODE AND AND GET RETURN VALUE IF WE HAVE THAT)



async def server():
    # Run test requests
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipmnet?id=4",
        "GET /shipmnet?id=3"
    )


    start = time.perf_counter() # 11:50 #Performance counter for benchmarking.

    for route in tests:
        result = await endpoint(route) #this await means > run this coroutine and wait for it to finish before moving on i.e await 
        print("Result back", result)
  

    end = time.perf_counter() # 11:53

    print(f"Time taken: {end - start:.2f}s")




# Run server
asyncio.run(
server()
)


# OUTPUT > 

# >> handling `GET /shipment?id=1` endpoint...
# << response from `GET /shipment?id=1` endpoint!
# Result back GET /shipment?id=1
# >> handling `PATCH /shipmnet?id=4` endpoint...
# << response from `PATCH /shipmnet?id=4` endpoint!
# Result back PATCH /shipmnet?id=4
# >> handling `GET /shipmnet?id=3` endpoint...
# << response from `GET /shipmnet?id=3` endpoint!
# Result back GET /shipmnet?id=3
# Time taken: 3.06s


# -------------------------------------------------------------------------------------------------------------------------------------

# WHY WE DIDN'T GET A LESS TIME TAKEN WITH OUR ASYNCHRONOUS CODE?

# because right now we are just making our code asynchronus i.e comaptabile with same, and because we await the same we are actually waiting here as well
# 
# if we remove await keyword we will got less time taken, and if that function is returing the value from the database, we dont get that back 