from uuid import UUID, uuid4
from datetime import datetime
from orders_service.app.models.order import Order, OrderStatus, OrderItem
from orders_service.app.repositories.order_repo import OrderRepo, orders_db

from typing import List

class OrderService:
    def __init__(self):
        self.repo = OrderRepo()

    def create_order(self, items: List[dict]):  
        total_price = sum(item['price'] for item in items)  
        items_parsed = [OrderItem(**item) for item in items] 
        order = Order(id=uuid4(),  
                      items=items_parsed, 
                      total_price=total_price, 
                      date=datetime.now(), 
                      status=OrderStatus.CREATED)
        return self.repo.add_order(order)

    def pay_order(self, id: UUID):
        order = self.repo.get_order(id)
        order.status = OrderStatus.PAID
        return self.repo.update_order(order)

    def cancel_order(self, id: UUID):
        order = self.repo.get_order(id)
        order.status = OrderStatus.CANCELED
        return self.repo.update_order(order)

    def confirm_order(self, id: UUID):
        order = self.repo.get_order(id)
        order.status = OrderStatus.CONFIRMED
        return self.repo.update_order(order)

    def request_delivery(self, id: UUID):
        order = self.repo.get_order(id)
        order.status = OrderStatus.DELIVERY_REQUESTED
        return self.repo.update_order(order)

    def complete_order(self, id: UUID):
        order = self.repo.get_order(id)
        order.status = OrderStatus.COMPLETED
        return self.repo.update_order(order)

    def get_orders(self):
        return orders_db  
