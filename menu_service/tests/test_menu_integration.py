import pytest
from fastapi.testclient import TestClient

from menu_service.app.main import app
from menu_service.app.endpoints import menu_router


@pytest.fixture(autouse=True)
def clear_db():
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
    yield
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_add_menu_item_and_get_menu(client):
    payload = {
        "name": "Latte",
        "description": "Coffee with milk",
        "price": 4.5,
        "type": "drink",
    }

    resp = client.post("/api/menu/", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["item"]["name"] == "Latte"

    menu_resp = client.get("/api/menu/")
    assert menu_resp.status_code == 200
    assert len(menu_resp.json()) == 1


def test_choose_item_adds_to_cart(client):
    payload = {
        "name": "Espresso",
        "description": "Strong coffee",
        "price": 3.0,
        "type": "drink",
    }

    resp = client.post("/api/menu/", json=payload)
    item_id = resp.json()["item"]["id"]

    choose_resp = client.post(f"/api/menu/choose_item/{item_id}")
    assert choose_resp.status_code == 200

    cart_resp = client.get("/api/menu/cart/")
    cart = cart_resp.json()["cart"]

    assert len(cart) == 1
    assert cart[0]["id"] == item_id


def test_get_drinks_returns_only_drinks(client):
    items = [
        {"name": "Cola", "description": "Soft drink", "price": 2.5, "type": "drink"},
        {"name": "Burger", "description": "Beef burger", "price": 8.0, "type": "food"},
    ]

    for item in items:
        client.post("/api/menu/", json=item)

    resp = client.get("/api/menu/drinks/")
    drinks = resp.json()["drinks"]

    assert len(drinks) == 1
    assert drinks[0]["name"] == "Cola"
