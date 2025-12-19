import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.endpoints import menu_router

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


def test_add_menu_item_creates_item_with_id(client):
    payload = {
        "name": "Latte",
        "description": "Coffee with milk",
        "price": 4.5,
        "type": "drink"
    }

    resp = client.post("/api/menu/", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["message"] == "Item added successfully"
    item = data["item"]

    assert item["name"] == payload["name"]
    assert item["description"] == payload["description"]
    assert item["price"] == payload["price"]
    assert item["type"] == payload["type"]

    assert "id" in item
    assert isinstance(item["id"], str)
    assert len(item["id"]) > 0


def test_get_menu_returns_all_items(client):
    items = [
        {
            "name": "Latte",
            "description": "Coffee with milk",
            "price": 4.5,
            "type": "drink",
        },
        {
            "name": "Burger",
            "description": "Beef burger",
            "price": 8.9,
            "type": "food",
        },
    ]

    for it in items:
        resp = client.post("/api/menu/", json=it)
        assert resp.status_code == 200

    resp = client.get("/api/menu/")
    assert resp.status_code == 200

    menu = resp.json()
    assert isinstance(menu, list)
    assert len(menu) == 2

    names = {m["name"] for m in menu}
    assert {"Latte", "Burger"} == names


def test_choose_item_adds_to_cart(client):
    payload = {
        "name": "Espresso",
        "description": "Strong coffee",
        "price": 3.0,
        "type": "drink",
    }
    resp = client.post("/api/menu/", json=payload)
    assert resp.status_code == 200
    item_id = resp.json()["item"]["id"]

    resp = client.post(f"/api/menu/choose_item/{item_id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["message"] == "Item has been added to cart"
    assert data["item"]["id"] == item_id

    cart_resp = client.get("/api/menu/cart/")
    assert cart_resp.status_code == 200
    cart_data = cart_resp.json()
    assert "cart" in cart_data
    assert len(cart_data["cart"]) == 1
    assert cart_data["cart"][0]["id"] == item_id


def test_choose_item_not_found(client):
    resp = client.post("/api/menu/choose_item/non-existing-id")
    assert resp.status_code == 200  

    data = resp.json()
    assert data["message"] == "Item not found."


def test_view_cart_initially_empty(client):
    resp = client.get("/api/menu/cart/")
    assert resp.status_code == 200

    data = resp.json()
    assert "cart" in data
    assert isinstance(data["cart"], list)
    assert len(data["cart"]) == 0


def test_get_drinks_filters_only_drinks(client):
    items = [
        {
            "name": "Cola",
            "description": "Soft drink",
            "price": 2.5,
            "type": "drink",
        },
        {
            "name": "Orange Juice",
            "description": "Fresh juice",
            "price": 3.0,
            "type": "drink",
        },
        {
            "name": "Pizza",
            "description": "Cheese pizza",
            "price": 10.0,
            "type": "food",
        },
    ]

    for it in items:
        resp = client.post("/api/menu/", json=it)
        assert resp.status_code == 200

    resp = client.get("/api/menu/drinks/")

    assert resp.status_code == 200

    data = resp.json()
    assert "drinks" in data
    drinks = data["drinks"]
    assert len(drinks) == 2

    drink_names = {d["name"] for d in drinks}
    assert drink_names == {"Cola", "Orange Juice"}
