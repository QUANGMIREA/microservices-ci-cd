from fastapi import APIRouter
from app.models.menu_item import MenuItem

router = APIRouter(prefix="/menu", tags=["Menu"])

# Unit tests mong chờ 2 list này chứa MenuItem (không phải dict)
menu_db: list[MenuItem] = []
cart_db: list[MenuItem] = []


@router.post("/")
def add_menu_item(item: MenuItem):
    menu_db.append(item)
    return {"message": "Item added successfully", "item": item.model_dump()}


@router.get("/")
def get_menu():
    # integration tests cần JSON serializable
    return [i.model_dump() for i in menu_db]


@router.post("/choose_item/{item_id}")
def choose_item(item_id: str):
    item = next((i for i in menu_db if i.id == item_id), None)
    if item is None:
        # test đang expect KHÔNG có dấu chấm
        return {"message": "Item not found"}

    cart_db.append(item)
    return {"message": "Item has been added to cart", "item": item.model_dump()}


@router.get("/cart/")
def view_cart():
    return {"cart": [i.model_dump() for i in cart_db]}


@router.get("/drinks/")
def get_drinks():
    drinks = [i for i in menu_db if i.type.lower() == "drink"]
    return {"drinks": [i.model_dump() for i in drinks]}
