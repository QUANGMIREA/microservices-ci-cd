from fastapi import FastAPI
from app.endpoints.menu_router import router as menu_router

app = FastAPI(title="Menu Service")
app.include_router(router, prefix="/api")
