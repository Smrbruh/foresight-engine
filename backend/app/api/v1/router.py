from fastapi import APIRouter

from app.api.v1.endpoints import agents, auth, metrics, predictions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
