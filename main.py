from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId
from fastapi import Response

from pymongo import MongoClient

app = FastAPI()

mongoClient = MongoClient("localhost", 27017)

db = mongoClient.mydatabase
items = db.items

class Category(str, Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    name: str
    price: float
    count: int
    category: Category

@app.post("/item", tags=["Items"])
def create_item(item: Item):
    item_dict = item.model_dump()
    inserted_item = items.insert_one(item_dict)
    return {"id": str(inserted_item.inserted_id)}

@app.get("/item/{id}", tags=["Items"])
def query_items_by_id(id: str):
    item = items.find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=404, detail=f"Id with {id} does not exist.")
    item["_id"] = str(item["_id"])
    return item

Selection = dict[str, str | int | float | Category | None]

@app.get("/items/", tags=["Items"])
def query_items_by_parameters(
        name: str | None = None,
        price: float | None = None,
        count: int | None = None,
        category: Category | None = None
):
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item["name"] == name,
                price is None or item["price"] == price,
                count is None or item["count"] == count,
                category is None or item["category"] == category
            )
        )
    selection = [item for item in items.find() if check_item(item)]
    
    for item in selection:
        item["_id"] = str(item["_id"])
    
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection
    }

@app.delete("/item/{id}", tags=["Items"])
def delete_item_by_id(id: str):
    items.delete_one({"_id": ObjectId(id)})
    return Response(status_code=204)

@app.put("/item/{id}", tags=["Items"])
def update_item_by_id(id: str, item: Item):
    found_item = items.find_one({"_id": ObjectId(id)})
    if not found_item:
        raise HTTPException(status_code=404, detail=f"Id with {id} does not exist.")
    
    item_dict = item.model_dump()
    items.update_one({"_id": ObjectId(id)}, {"$set": item_dict})
    return Response(status_code=204)
