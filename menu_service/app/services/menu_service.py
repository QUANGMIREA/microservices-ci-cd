from app.models.menu_item import MenuItem
from fastapi import APIRouter
from pydantic import BaseModel

#class MenuItem(BaseModel):
#    name: str
#    description: str
#    price: float

router = APIRouter(prefix="/menu", tags=["Menu"])

menu_db = [] 

@router.post("/")
def add_menu_item(item: MenuItem):
    menu_db.append(item)
    return {"message": "Item added successfully", "item": item}
