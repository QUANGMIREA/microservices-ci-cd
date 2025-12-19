import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.endpoints.menu_router as menu_router  # QUAN TRỌNG: import module đúng


@pytest.fixture(autouse=True)
def _reset_in_memory_db():
    # Clear trước mỗi test
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()
    yield
    # Clear sau mỗi test
    menu_router.menu_db.clear()
    menu_router.cart_db.clear()


@pytest.fixture
def client():
    # TestClient sẽ chạy startup => nếu startup có seed data, ta clear lại NGAY SAU khi startup chạy
    with TestClient(app) as c:
        menu_router.menu_db.clear()
        menu_router.cart_db.clear()
        yield c
