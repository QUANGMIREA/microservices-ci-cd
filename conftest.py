import pytest

@pytest.fixture(autouse=True)
def _reset_inmemory_dbs():
    """
    Chạy trước MỌI test.
    Reset đúng module menu_router mà app đang dùng.
    """
    from app.endpoints import menu_router

    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
    yield
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
