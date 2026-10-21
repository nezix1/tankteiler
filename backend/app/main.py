from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="TankTeiler API",
    description="Trip cost calculations and recorded fuel prices.",
    version="0.1.0",
)
app.include_router(router)
