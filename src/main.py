from fastapi import FastAPI

from src.config import get_project_settings
from src.tron.routers import tron_router

app = FastAPI(
    title="Tron Info Test",
    version=get_project_settings().VERSION,
)

available_routers = [
    tron_router,
]

for router in available_routers:
    app.include_router(router)
