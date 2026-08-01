from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, users, datasets, processing, analytics, ai

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(processing.router, prefix="/datasets", tags=["processing"])
api_router.include_router(analytics.router, prefix="/datasets", tags=["analytics"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
