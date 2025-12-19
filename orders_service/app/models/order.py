from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
import enum
from typing import List

class OrderStatus(enum.Enum):
    CREATED = 'created'
    PAID = 'paid'
    CANCELED = 'canceled'
    CONFIRMED = 'confirmed'  
    DELIVERY_REQUESTED = 'delivery_requested'  
    DELIVERED = 'delivered'  
    COMPLETED = 'completed'  

class OrderItem(BaseModel):
    item: str
    price: float

class Order(BaseModel):
    id: UUID
    items: List[OrderItem]  
    total_price: float      
    date: datetime
    status: OrderStatus