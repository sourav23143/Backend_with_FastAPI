import time
from rich import print


def endpoint(route: str) -> str:
    print(f">> handling `{route}` endpoint...")

    # emulate database delay
    time.sleep(1)

    print(f"<< response from `{route}` endpoint!")





def server():
    # Run test requests
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipmnet?id=4",
        "GET /shipmnet?id=3"
    )


    start = time.perf_counter() # 11:50 #Performance counter for benchmarking.

    for route in tests:
        endpoint(route)

    end = time.perf_counter() # 11:53

    print(f"Time taken: {end - start:.2f}s")




# Run server
server()


# OUTPUT > 

# >> handling `GET /shipment?id=1` endpoint...
# << response from `GET /shipment?id=1` endpoint!
# >> handling `PATCH /shipmnet?id=4` endpoint...
# << response from `PATCH /shipmnet?id=4` endpoint!
# >> handling `GET /shipmnet?id=3` endpoint...
# << response from `GET /shipmnet?id=3` endpoint!
# Time taken: 3.07s


# RIGHT NOW WE ARE WATING FOR ONE REQUEST TO BE HANDLED BEFORE MOVING TO ANOTHER ONE WHICH IS SYNCHRONOUS IN NATURE