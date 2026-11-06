from contextlib import asynccontextmanager
from fastapi import FastAPI

from rich import print, panel # to create border around message and also to add color to the message



@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green", style="bold green"))
    yield
    print(panel.Panel("...stopped!", border_style="red", style="bold red"))




app = FastAPI(lifespan=lifespan_handler)


@app.get("/")
def read_root():
    return {"detail": "Server running..."}




# (.venv) PS C:\Users\ASUS\Backend_with_FastAPI\07_SQL_Model\03_SQL_Model> fastapi dev test.py

#  ⚡️ Starting FastAPI in development mode
 
#  🐍 Using import string: test:app
 
#  🌐 Server started at http://127.0.0.1:8000
#     Documentation at http://127.0.0.1:8000/docs
 
#   Logs:
 
#  ▕  Will watch for changes in these directories: ['C:\\Users\\ASUS\\Backend_with_FastAPI\\07_SQL_Model\\03_SQL_Model']
#  ▕  Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
#  ▕  Started reloader process [25044] using WatchFiles
#  ▕  Started server process [8820]
#  ▕  Waiting for application startup.
# ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ Server started...                                                                                                                            │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
#  ▕  Application startup complete.

#  ▕  Shutting down
#  ▕  Waiting for application shutdown.
# ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ ...stopped!                                                                                                                                  │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
#  ▕  Application shutdown complete.
#  ▕  Finished server process [8820]
#  ▕  Stopping reloader process [25044]
