# pip install unicorn
# pip install fastapi
from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# commands cmd:
# # uvicorn working:app --reload

# # doc -> http://127.0.0.1:8000/docs

# @app.get("/")
# def home():
#     return {"Data": "Test"}

# @app.get("/about")
# def about():
#     return {"Data": "Test"}

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}


@app.get("/get-item/{item_id}/")
def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view", gt=0)):
    return inventory[item_id]


@app.get("/get-by-name/{item_id}")
def get_item(name: str = Query(None, title="Name", description="Name of item.")):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        return {"Data": "Not found"}


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists."}

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exists."}

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete.")):
    if item_id not in inventory:
        return {"Error": "ID does not exist."}
    del inventory[item_id]
    return {"Success": "Item deleted!"}
