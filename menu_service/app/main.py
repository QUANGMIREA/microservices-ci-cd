from fastapi import FastAPI
from menu_service.app.endpoints.menu_router import router

app = FastAPI(title="Menu Service")
app.include_router(router, prefix="/api")
