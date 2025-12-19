import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.endpoints import menu_router


@pytest.fixture
def client():
    # đảm bảo startup chạy trước (nếu có), rồi mới clear DB giả lập
    with TestClient(app) as c:
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
        yield c
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
