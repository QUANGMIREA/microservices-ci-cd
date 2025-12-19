import pytest
from fastapi.testclient import TestClient

# Import app + menu_router đúng theo cách bạn chạy pytest
# (CI của bạn đang chạy trong working-directory: menu_service)
from app.main import app
from app.endpoints import menu_router


@pytest.fixture(autouse=True)
def clear_db():
    # clear trước mỗi test
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()

    yield

    # clear sau mỗi test (đề phòng)
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()


@pytest.fixture
def client():
    return TestClient(app)
