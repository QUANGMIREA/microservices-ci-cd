from fastapi import APIRouter
from app.models.menu_item import MenuItem

router = APIRouter(prefix="/menu", tags=["Menu"])

menu_db: list[MenuItem] = []
cart_db: list[MenuItem] = []


@router.post("/")
def add_menu_item(item: MenuItem):
    menu_db.append(item)
    return {"message": "Item added successfully", "item": item}


@router.get("/")
def get_menu():
    return menu_db


@router.post("/choose_item/{item_id}")
def choose_item(item_id: str):
    item = next((i for i in menu_db if i.id == item_id), None)
    if item is None:
        # chú ý dấu chấm .
        return {"message": "Item not found."}

    cart_db.append(item)
    return {"message": "Item has been added to cart", "item": item}


@router.get("/cart/")
def view_cart():
    return {"cart": cart_db}


@router.get("/drinks/")
def get_drinks():
    # giữ MenuItem object, không dùng item.get(...)
    drinks = [item for item in menu_db if item.type.lower() == "drink"]
    return {"drinks": drinks}
