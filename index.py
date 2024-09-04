import os
import uvicorn
from fastapi import FastAPI
from routes.note import note
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.db import conn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note)

if __name__ == "__main__":
    # Get the port from the environment variable PORT (default to 8000 if not set)
    port = int(os.getenv('PORT', 8000))
    
    # Start the server with the specified host and port
    uvicorn.run(app, host="0.0.0.0", port=port)
