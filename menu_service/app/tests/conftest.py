import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.endpoints import menu_router


@pytest.fixture
def client():
    # TestClient sẽ chạy startup => nếu startup seed data thì clear phải làm SAU khi tạo client
    with TestClient(app) as c:
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
        yield c
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
