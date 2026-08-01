from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import RequestIDMiddleware, RequestTimingMiddleware
from app.core.exceptions import add_exception_handlers
from app.api.v1.api import api_router
from app.core.logger import setup_logging

setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    add_exception_handlers(app)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
