import pytest
from fastapi.testclient import TestClient

from orders_service.app.main import app
from orders_service.app.repositories.order_repo import orders_db
from orders_service.app.models.order import OrderStatus


@pytest.fixture(autouse=True)
def clear_orders():
    orders_db.clear()
    yield
    orders_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_order(client):
    payload = {
        "items": [
            {"item": "Pizza", "price": 10.0},
            {"item": "Cola", "price": 3.0},
        ]
    }

    resp = client.post("/api/orders/", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["total_price"] == 13.0
    assert data["status"] == OrderStatus.CREATED.value


def test_full_order_lifecycle(client):
    payload = {"items": [{"item": "Steak", "price": 20.0}]}

    create_resp = client.post("/api/orders/", json=payload)
    order_id = create_resp.json()["id"]

    client.post(f"/api/orders/{order_id}/pay")
    client.post(f"/api/orders/{order_id}/confirm")
    client.post(f"/api/orders/{order_id}/request_delivery")
    client.post(f"/api/orders/{order_id}/complete")

    assert orders_db[0].status == OrderStatus.COMPLETED


def test_cancel_order(client):
    payload = {"items": [{"item": "Burger", "price": 7.0}]}

    create_resp = client.post("/api/orders/", json=payload)
    order_id = create_resp.json()["id"]

    cancel_resp = client.post(f"/api/orders/{order_id}/cancel")
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == OrderStatus.CANCELED.value


def test_non_existing_order_returns_404(client):
    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    resp = client.post(f"/api/orders/{fake_id}/pay")
    assert resp.status_code == 404
