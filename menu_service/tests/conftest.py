import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.endpoints import menu_router


@pytest.fixture
def client():
    # Dùng context manager để đảm bảo startup/shutdown chạy đúng
    with TestClient(app) as c:
        # QUAN TRỌNG: clear SAU khi startup chạy
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
        yield c
        # clear sau test luôn cho chắc
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
