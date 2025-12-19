import pytest
from uuid import uuid4
from datetime import datetime

from app.services.order_service import OrderService
from app.repositories.order_repo import orders_db
from app.models.order import OrderStatus, Order


@pytest.fixture(autouse=True)
def clear_orders_db():

    orders_db.clear()
    yield
    orders_db.clear()


@pytest.fixture
def service():
    return OrderService()


def test_create_order_builds_correct_order(service):
    items = [
        {"item": "Pizza", "price": 10.0},
        {"item": "Cola", "price": 3.5},
    ]

    order = service.create_order(items)

    assert isinstance(order, Order)
    assert order.id is not None
    assert order.total_price == 13.5
    assert len(order.items) == 2
    assert order.items[0].item == "Pizza"
    assert order.items[1].item == "Cola"
    assert order.status == OrderStatus.CREATED
    assert isinstance(order.date, datetime)
    assert len(orders_db) == 1
    assert orders_db[0].id == order.id


def test_pay_order_changes_status_to_paid(service):
    order = service.create_order(
        [{"item": "Burger", "price": 7.0}]
    )

    paid = service.pay_order(order.id)

    assert paid.status == OrderStatus.PAID
    assert orders_db[0].status == OrderStatus.PAID


def test_cancel_order_changes_status_to_canceled(service):
    order = service.create_order(
        [{"item": "Sushi", "price": 15.0}]
    )

    canceled = service.cancel_order(order.id)

    assert canceled.status == OrderStatus.CANCELED
    assert orders_db[0].status == OrderStatus.CANCELED


def test_confirm_order_after_pay(service):
    order = service.create_order(
        [{"item": "Tea", "price": 3.0}]
    )

    service.pay_order(order.id)
    confirmed = service.confirm_order(order.id)

    assert confirmed.status == OrderStatus.CONFIRMED
    assert orders_db[0].status == OrderStatus.CONFIRMED


def test_request_delivery_and_complete_flow(service):
    order = service.create_order(
        [{"item": "Steak", "price": 20.0}]
    )

    service.pay_order(order.id)
    service.confirm_order(order.id)
    delivery_requested = service.request_delivery(order.id)
    assert delivery_requested.status == OrderStatus.DELIVERY_REQUESTED
    assert orders_db[0].status == OrderStatus.DELIVERY_REQUESTED

    completed = service.complete_order(order.id)
    assert completed.status == OrderStatus.COMPLETED
    assert orders_db[0].status == OrderStatus.COMPLETED


def test_pay_non_existing_order_raises_keyerror(service):
    random_id = uuid4()

    with pytest.raises(KeyError):
        service.pay_order(random_id)


def test_cancel_non_existing_order_raises_keyerror(service):
    random_id = uuid4()

    with pytest.raises(KeyError):
        service.cancel_order(random_id)


def test_get_orders_returns_all_orders(service):

    o1 = service.create_order([{"item": "Latte", "price": 4.0}])
    o2 = service.create_order(
        [{"item": "Tea", "price": 3.0}, {"item": "Cookie", "price": 2.0}]
    )

    orders = service.get_orders()

    assert len(orders) == 2
    ids = {o.id for o in orders}
    assert ids == {o1.id, o2.id}
    totals = sorted(o.total_price for o in orders)
    assert totals == [4.0, 5.0]
