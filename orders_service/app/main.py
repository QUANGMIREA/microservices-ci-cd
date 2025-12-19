from fastapi import FastAPI
from orders_service.app.endpoints.order_router import router

app = FastAPI(title="Order Service")
app.include_router(router, prefix="/api")
