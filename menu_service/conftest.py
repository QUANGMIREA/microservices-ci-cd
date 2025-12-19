import pytest
from fastapi.testclient import TestClient

from app.main import app


def _clear_router_state(router_mod):
    router_mod.menu_db.clear()
    router_mod.cart_db.clear()


@pytest.fixture(autouse=True)
def clear_db():
    """
    Clear menu_db/cart_db cho mọi đường import có thể xảy ra.
    Lý do: có nơi import app.endpoints.menu_router, có nơi import menu_service.app.endpoints.menu_router
    => nếu chỉ clear 1 cái thì cái còn lại vẫn giữ dữ liệu.
    """
    # 1) đường import phổ biến khi chạy pytest trong menu_service/
    try:
        from app.endpoints import menu_router as r1
        _clear_router_state(r1)
    except Exception:
        r1 = None

    # 2) đường import kiểu package menu_service (nếu test dùng kiểu này)
    try:
        from menu_service.app.endpoints import menu_router as r2
        _clear_router_state(r2)
    except Exception:
        r2 = None

    yield

    # clear lại lần nữa sau test
    if r1:
        _clear_router_state(r1)
    if r2 and (r2 is not r1):
        _clear_router_state(r2)


@pytest.fixture
def client():
    return TestClient(app)
