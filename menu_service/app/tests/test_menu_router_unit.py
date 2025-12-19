import pytest

from app.endpoints import menu_router
from app.models.menu_item import MenuItem


@pytest.fixture(autouse=True)
def clear_db():

    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
    yield
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()


def test_add_menu_item_appends_to_menu_db_and_returns_item():
    item = MenuItem(
        name="Latte",
        description="Coffee with milk",
        price=4.5,
        type="drink",
    )

    response = menu_router.add_menu_item(item)

    assert len(menu_router.menu_db) == 1
    assert menu_router.menu_db[0] is item

    assert response["message"] == "Item added successfully"
    assert response["item"] is item


def test_get_menu_returns_current_menu_list():
    item1 = MenuItem(
        name="Latte",
        description="Coffee with milk",
        price=4.5,
        type="drink",
    )
    item2 = MenuItem(
        name="Burger",
        description="Beef burger",
        price=8.9,
        type="food",
    )

    menu_router.add_menu_item(item1)
    menu_router.add_menu_item(item2)

    menu = menu_router.get_menu()

    assert isinstance(menu, list)
    assert len(menu) == 2
    assert menu[0] is item1
    assert menu[1] is item2


def test_choose_item_adds_existing_item_to_cart():
    item = MenuItem(
        name="Espresso",
        description="Strong coffee",
        price=3.0,
        type="drink",
    )
    menu_router.add_menu_item(item)

    response = menu_router.choose_item(item.id)

    assert response["message"] == "Item has been added to cart"
    assert response["item"] is item

    assert len(menu_router.cart_db) == 1
    assert menu_router.cart_db[0] is item


def test_choose_item_returns_not_found_message_for_invalid_id():
    fake_id = "non-existing-id"

    response = menu_router.choose_item(fake_id)

    assert response["message"] == "Item not found."
    assert len(menu_router.cart_db) == 0


def test_view_cart_returns_current_cart_contents():
    item1 = MenuItem(
        name="Cola",
        description="Soft drink",
        price=2.5,
        type="drink",
    )
    item2 = MenuItem(
        name="Pizza",
        description="Cheese pizza",
        price=10.0,
        type="food",
    )

    menu_router.cart_db.append(item1)
    menu_router.cart_db.append(item2)

    response = menu_router.view_cart()

    assert "cart" in response
    cart = response["cart"]
    assert len(cart) == 2
    assert cart[0] is item1
    assert cart[1] is item2


def test_get_drinks_filters_only_items_with_type_drink():
    drink1 = MenuItem(
        name="Cola",
        description="Soft drink",
        price=2.5,
        type="drink",
    )
    drink2 = MenuItem(
        name="Orange Juice",
        description="Fresh juice",
        price=3.0,
        type="drink",
    )
    food = MenuItem(
        name="Pizza",
        description="Cheese pizza",
        price=10.0,
        type="food",
    )

    menu_router.menu_db.extend([drink1, drink2, food])

    response = menu_router.get_drinks()

    assert "drinks" in response
    drinks = response["drinks"]

    assert len(drinks) == 2
    assert drink1 in drinks
    assert drink2 in drinks
    assert food not in drinks
