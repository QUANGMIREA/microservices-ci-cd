from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from pydantic import BaseModel
from typing import List
from orders_service.app.services.order_service import OrderService


router = APIRouter(prefix="/orders", tags=["Orders"])

class OrderItem(BaseModel):
    item: str
    price: float

class OrderRequest(BaseModel):
    items: List[OrderItem] 

@router.post("/")
def create_order(order: OrderRequest, service: OrderService = Depends(OrderService)):
    return service.create_order([item.model_dump() for item in order.items])


@router.post("/{id}/pay")
def pay_order(id: UUID, service: OrderService = Depends(OrderService)):
    try:
        return service.pay_order(id)
    except KeyError:
        raise HTTPException(404, "Order not found")

@router.post("/{id}/cancel")
def cancel_order(id: UUID, service: OrderService = Depends(OrderService)):
    try:
        return service.cancel_order(id)
    except KeyError:
        raise HTTPException(404, "Order not found")

@router.get("/")
def get_orders(service: OrderService = Depends(OrderService)):
    return service.get_orders()

@router.post("/{id}/confirm")
def confirm_order(id: UUID, service: OrderService = Depends(OrderService)):
    try:
        return service.confirm_order(id)
    except KeyError:
        raise HTTPException(404, "Order not found")

@router.post("/{id}/request_delivery")
def request_delivery(id: UUID, service: OrderService = Depends(OrderService)):
    try:
        return service.request_delivery(id)
    except KeyError:
        raise HTTPException(404, "Order not found")

@router.post("/{id}/complete")
def complete_order(id: UUID, service: OrderService = Depends(OrderService)):
    try:
        return service.complete_order(id)
    except KeyError:
        raise HTTPException(404, "Order not found")
