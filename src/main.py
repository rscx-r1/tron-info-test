from fastapi import FastAPI

from src.config import project_settings

app = FastAPI(
    title="Tron Info Test",
    version=project_settings.VERSION,
)

available_routers = []

for router in available_routers:
    app.include_router(router)
