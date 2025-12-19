from fastapi import APIRouter
from app.models.menu_item import MenuItem
import uuid

router = APIRouter(prefix="/menu", tags=["Menu"])

menu_db: list[dict] = []
cart_db: list[dict] = []


@router.post("/")
def add_menu_item(item: MenuItem):
    item_dict = item.dict()

    # đảm bảo có id
    if not item_dict.get("id"):
        item_dict["id"] = str(uuid.uuid4())

    menu_db.append(item_dict)
    return {"message": "Item added successfully", "item": item_dict}


@router.get("/")
def get_menu():
    return menu_db


@router.post("/choose_item/{item_id}")
def choose_item(item_id: str):
    item = next((i for i in menu_db if i["id"] == item_id), None)
    if item is None:
        return {"message": "Item not found"}

    cart_db.append(item)
    return {"message": "Item has been added to cart", "item": item}


@router.get("/cart/")
def view_cart():
    return {"cart": cart_db}


@router.get("/drinks/")
def get_drinks():
    drinks = [i for i in menu_db if i["type"].lower() == "drink"]
    return {"drinks": drinks}
