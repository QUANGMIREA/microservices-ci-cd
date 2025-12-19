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
