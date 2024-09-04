from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.db import conn

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request, query: str = "", important_filter: str = ""):
    search_filter = {}

    if query:
        search_filter["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"desc": {"$regex": query, "$options": "i"}}
        ]

    if important_filter:
        if important_filter == "important":
            search_filter["important"] = True
        elif important_filter == "not_important":
            search_filter["important"] = False

    # Find and sort the notes so pinned notes appear at the top
    docs = conn.notes.notes.find(search_filter).sort([("pinned", -1), ("_id", -1)])
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"],
            "pinned": doc.get("pinned", False)  # Default to False if not set
        })

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    formDict["pinned"] = True if formDict.get("pinned") == "on" else False  # Handle pinned field
    conn.notes.notes.insert_one(formDict)
    return RedirectResponse("/", status_code=303)


@note.post("/delete/{id}")
async def delete_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid note ID format")

    result = conn.notes.notes.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return RedirectResponse("/", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Note not found")


@note.post("/update/{id}")
async def update_item(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid note ID format")

    form = await request.form()
    update_data = {
        "title": form.get("title"),
        "desc": form.get("desc"),
        "important": form.get("important") == "on",
        "pinned": form.get("pinned") == "on"  # Handle pinned field
    }

    result = conn.notes.notes.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    return RedirectResponse("/", status_code=303)


@note.post("/pin/{id}")
async def pin_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid note ID format")

    note = conn.notes.notes.find_one({"_id": ObjectId(id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    new_pinned_status = not note.get("pinned", False)
    conn.notes.notes.update_one({"_id": ObjectId(id)}, {"$set": {"pinned": new_pinned_status}})

    return RedirectResponse("/", status_code=303)