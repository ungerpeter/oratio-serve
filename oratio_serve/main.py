from fastapi import FastAPI
from oratio_serve.api.v1.endpoints import router as api_router
from oratio_serve.core import config, logger

app = FastAPI(
    title="Oratio Serve",
    version="0.1.0",
    description="A REST API inference service for speech AI models."
)

app.include_router(api_router, prefix="/api/v1")

logger.setup_logging()