

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

    
    requests = [ 
        asyncio.create_task(endpoint(route))  #Schedule the execution of a coroutine object in a spawn task.
        for route in tests
    ]  # so by this we have list of all of our task

     # And when we have these requests, that is all of the tasks we can run them in asynchronus fashion (i.e instead of wating work on another task)

    # result = asyncio.wait() #Wait for the Futures or Tasks given by fs to complete. # result will be tuple, so we have to unpack it here # ) # CoroutineType[Any, Any, tuple[set[_FT@wait], set[_FT@wait]]]

    done, pending = await asyncio.wait(requests) # done > task that are finished, / pending >task that are pending 


    # so by this we run all of task in a efficient manner, and now we can loop over  the finish task , in this case we will not have any pending tasks

    for task in done:
        print("Result:", task.result())



    end = time.perf_counter() # 11:53

    print(f"Time taken: {end - start:.2f}s")




# Run server
asyncio.run(
server()
)


# OUTPUT > 

# >> handling `GET /shipment?id=1` endpoint...
# >> handling `PATCH /shipmnet?id=4` endpoint...
# >> handling `GET /shipmnet?id=3` endpoint...
# << response from `GET /shipment?id=1` endpoint!
# << response from `PATCH /shipmnet?id=4` endpoint!
# << response from `GET /shipmnet?id=3` endpoint!
# Result: PATCH /shipmnet?id=4
# Result: GET /shipment?id=1
# Result: GET /shipmnet?id=3
# Time taken: 1.09s


# NOW WE HAVE ALL OF THEM HANDLE IN SECONDS, 
# IF WE INSPECT THE LOGS, WE CAN SEE IT HANDLES ALL OF THE ENDPOINTS TOGETHER (I.E ACCEPTS THE REQUESTS) AND THEN WAIT FOR EMULATED DATABASE DELAY AND THEN SEND THE RESPONSE BACK
# AND THEN WE GET RESULT BACK  


# SO ESSENTIALLY WE CREATE A TASK, WE ACTUALLY RUN IT IN EFFICIENT MANNER 
# I,E WHEN WE HAVE AWAIT LIKE THIS > await asyncio.sleep(1)
# INSTED OF WATING FOR IT WE CAN GO AHEAD AND RUN ANOTHER TASK 