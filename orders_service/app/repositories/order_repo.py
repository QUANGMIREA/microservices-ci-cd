from uuid import UUID
from orders_service.app.models.order import Order


orders_db = []

class OrderRepo:
    def add_order(self, order: Order) -> Order:
        orders_db.append(order)
        return order

    def get_order(self, id: UUID) -> Order:
        for order in orders_db:
            if order.id == id:
                return order
        raise KeyError("Order not found")

    def update_order(self, order: Order) -> Order:
        for idx, o in enumerate(orders_db):
            if o.id == order.id:
                orders_db[idx] = order
                return order
        raise KeyError("Order not found")
