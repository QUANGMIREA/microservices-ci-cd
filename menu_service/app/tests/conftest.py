import pytest
from fastapi.testclient import TestClient

from menu_service.app.main import app
from menu_service.app.endpoints.menu_router import menu_db, cart_db


@pytest.fixture(autouse=True)
def clear_db():
    """
    Reset database BEFORE and AFTER every test
    """
    menu_db.clear()
    cart_db.clear()
    yield
    menu_db.clear()
    cart_db.clear()


@pytest.fixture
def client():
    return TestClient(app)
