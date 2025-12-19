from fastapi import APIRouter
from app.models.menu_item import MenuItem

router = APIRouter(prefix="/menu", tags=["Menu"])

menu_db: list[MenuItem] = []
cart_db: list[MenuItem] = []


@router.post("/")
def add_menu_item(item: MenuItem):
    menu_db.append(item)
    # UNIT TEST muốn item là object y hệt
    return {"message": "Item added successfully", "item": item}


@router.get("/")
def get_menu():
    # UNIT TEST muốn trả list object
    return menu_db


@router.post("/choose_item/{item_id}")
def choose_item(item_id: str):
    item = next((i for i in menu_db if i.id == item_id), None)
    if item is None:
        # TEST muốn có dấu chấm
        return {"message": "Item not found."}

    cart_db.append(item)
    return {"message": "Item has been added to cart", "item": item}


@router.get("/cart/")
def view_cart():
    # UNIT TEST muốn cart chứa object
    return {"cart": cart_db}


@router.get("/drinks/")
def get_drinks():
    drinks = [i for i in menu_db if i.type.lower() == "drink"]
    return {"drinks": drinks}
