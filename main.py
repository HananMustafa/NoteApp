#from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from pymongo import MongoClient
app = FastAPI()



conn = MongoClient("mongodb+srv://ammodisultan123:0147852369@cluster0.cubfw.mongodb.net")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs= []
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "note": doc["note"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs" : newDocs})

