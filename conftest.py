import pytest

@pytest.fixture(autouse=True)
def _reset_inmemory_dbs():
    # Nếu module menu_router tồn tại thì reset, không thì bỏ qua (để orders_service không chết)
    try:
        from menu_service.app.endpoints import menu_router
    except Exception:
        yield
        return

    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
    yield
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
