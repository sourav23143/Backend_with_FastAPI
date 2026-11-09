

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


    # Task Group
    # and since this taskgroup is context manage, so we can use it with statement
    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(endpoint(route)) # to create task # and because this is a asynchronus fn so we have to make this block of code async comapatible as well 
            for route in tests
        ]
        # and that will be task we create > and insted of wating it that we have done before it will be run for us by the task group with efficient wating 
        # And as we add coroutine on multiple coroutines to this task group, they will be run efficiently , i.e whenever a task is wating for any I/O(let say pur database delay ), it can go ahead and do another task as well 
        print(await tasks[0]) #await to get reseult from tasks[0] coroutine

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
# GET /shipment?id=1
# Time taken: 1.06s



# WE GET SAME BEHAVIOUR AS EARLIER, I.E AS SOON AS WE ADD COROUTINE, THAT IS create_task, IT WILL BE RUN AND IF WE HAVE MULTIPLE TASKS IN THE GROUP, IT WILL BE HAVING EFFICIENT BEHAVIOUR WHICH WE REQUIRED
# AS WE ADD COROUTINE, THAT IS CREATE A TASK IN TASK GROUP,  THE COROUTINE GET AWAITED, AND IF THERE IS WAIT LIKE DATABASE DELAY, IT GOES AHEAD AND WORKS ON ANOTHER TASK IN THE GROUP 


