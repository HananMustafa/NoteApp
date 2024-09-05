# import os
# import uvicorn
# from fastapi import FastAPI
# from routes.note import note
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from config.db import conn

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(note)

# if __name__ == "__main__":
#     port = int(os.getenv('PORT', 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)


from fastapi import FastAPI
from routes.note import note
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.db import conn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(note)