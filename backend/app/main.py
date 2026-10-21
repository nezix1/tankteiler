from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="TankTeiler API",
    description="Trip cost calculations and recorded fuel prices.",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.include_router(router)
