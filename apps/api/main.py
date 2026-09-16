from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.middleware import ApiKeyMiddleware, RateLimitMiddleware, RequestIdMiddleware
from apps.api.routes import router
from jdmatcher.logging_config import configure_logging
from jdmatcher.settings import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="JD Matcher API",
        version="1.3.0",
        lifespan=lifespan,
    )
    application.add_middleware(RateLimitMiddleware)
    application.add_middleware(ApiKeyMiddleware)
    application.add_middleware(RequestIdMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router, prefix=settings.api_prefix)
    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)
