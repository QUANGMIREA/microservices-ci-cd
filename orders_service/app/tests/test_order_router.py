import pytest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.repositories.order_repo import orders_db
from app.models.order import OrderStatus


@pytest.fixture(autouse=True)
def clear_orders_db():
    orders_db.clear()
    yield
    orders_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_order_creates_order_with_correct_total_and_status_created(client):
    payload = {
        "items": [
            {"item": "Pizza", "price": 10.0},
            {"item": "Cola", "price": 3.5},
        ]
    }

    resp = client.post("/api/orders/", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert "id" in data
    assert isinstance(data["id"], str)
    assert data["total_price"] == 13.5
    assert data["status"] == OrderStatus.CREATED.value  # 'created'

    assert len(data["items"]) == 2
    assert data["items"][0]["item"] == "Pizza"
    assert data["items"][1]["item"] == "Cola"


def test_pay_order_changes_status_to_paid(client):
    payload = {
        "items": [
            {"item": "Burger", "price": 7.0},
        ]
    }
    create_resp = client.post("/api/orders/", json=payload)
    assert create_resp.status_code == 200
    order_id = create_resp.json()["id"]

    pay_resp = client.post(f"/api/orders/{order_id}/pay")
    assert pay_resp.status_code == 200

    paid_order = pay_resp.json()
    assert paid_order["id"] == order_id
    assert paid_order["status"] == OrderStatus.PAID.value


def test_cancel_order_changes_status_to_canceled(client):
    payload = {
        "items": [
            {"item": "Sushi", "price": 15.0},
        ]
    }
    create_resp = client.post("/api/orders/", json=payload)
    assert create_resp.status_code == 200
    order_id = create_resp.json()["id"]

    cancel_resp = client.post(f"/api/orders/{order_id}/cancel")
    assert cancel_resp.status_code == 200

    canceled_order = cancel_resp.json()
    assert canceled_order["status"] == OrderStatus.CANCELED.value


@pytest.mark.parametrize(
    "endpoint_suffix",
    ["pay", "cancel", "confirm", "request_delivery", "complete"],
)
def test_actions_on_non_existing_order_return_404(client, endpoint_suffix):
    """
    ??????????? ?????????? ????: ?????????, ??? ??? ??????????????? ??????
    ??? ?????? ?????????? 404.
    """
    random_id = uuid4()
    resp = client.post(f"/api/orders/{random_id}/{endpoint_suffix}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Order not found"


def test_full_order_lifecycle_changes_statuses_in_repo(client):
    """
    ??????????? ????????? ????:
    created -> paid -> confirmed -> delivery_requested -> completed.
    ????????? ??????? ???????? ????? ?????????? orders_db.
    """
    payload = {
        "items": [
            {"item": "Steak", "price": 20.0},
            {"item": "Water", "price": 2.0},
        ]
    }
    # 1. Create
    create_resp = client.post("/api/orders/", json=payload)
    assert create_resp.status_code == 200
    order_id = create_resp.json()["id"]

    assert len(orders_db) == 1
    assert orders_db[0].status == OrderStatus.CREATED

    # 2. Pay
    pay_resp = client.post(f"/api/orders/{order_id}/pay")
    assert pay_resp.status_code == 200
    assert orders_db[0].status == OrderStatus.PAID

    # 3. Confirm
    confirm_resp = client.post(f"/api/orders/{order_id}/confirm")
    assert confirm_resp.status_code == 200
    assert orders_db[0].status == OrderStatus.CONFIRMED

    # 4. Request delivery
    delivery_resp = client.post(f"/api/orders/{order_id}/request_delivery")
    assert delivery_resp.status_code == 200
    assert orders_db[0].status == OrderStatus.DELIVERY_REQUESTED

    # 5. Complete
    complete_resp = client.post(f"/api/orders/{order_id}/complete")
    assert complete_resp.status_code == 200
    assert orders_db[0].status == OrderStatus.COMPLETED


def test_get_orders_returns_all_orders(client):

    payload1 = {
        "items": [
            {"item": "Latte", "price": 4.0},
        ]
    }
    payload2 = {
        "items": [
            {"item": "Tea", "price": 3.0},
            {"item": "Cookie", "price": 2.0},
        ]
    }

    resp1 = client.post("/api/orders/", json=payload1)
    resp2 = client.post("/api/orders/", json=payload2)
    assert resp1.status_code == 200
    assert resp2.status_code == 200

    list_resp = client.get("/api/orders/")
    assert list_resp.status_code == 200

    orders = list_resp.json()
    assert isinstance(orders, list)
    assert len(orders) == 2

    totals = sorted(o["total_price"] for o in orders)
    assert totals == [4.0, 5.0]
