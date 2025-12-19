import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.endpoints import menu_router


@pytest.fixture(autouse=True)
def clear_in_memory_db():
    # reset data before each test
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)
