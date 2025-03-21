from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.png")

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

items = []

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for idx, item in enumerate(items):
        if item.id == item_id:
            items[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for idx, item in enumerate(items):
        if item.id == item_id:
            items.pop(idx)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")