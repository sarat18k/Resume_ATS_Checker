import time
import uuid
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from jdmatcher.settings import get_settings


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class ApiKeyMiddleware(BaseHTTPMiddleware):
    _PUBLIC_PATHS = {"/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next) -> Response:
        settings = get_settings()
        path = request.url.path
        if not settings.api_auth_enabled:
            return await call_next(request)
        if path.endswith("/health") or path in self._PUBLIC_PATHS:
            return await call_next(request)

        provided = request.headers.get("X-API-Key") or request.headers.get(
            "Authorization", ""
        ).removeprefix("Bearer ").strip()
        if provided != settings.api_key:
            return JSONResponse(status_code=401, content={"detail": "Invalid API key."})
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        settings = get_settings()
        if request.url.path.endswith("/health"):
            return await call_next(request)

        client_host = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - 60
        bucket = self._hits[client_host]
        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= settings.rate_limit_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again shortly."},
            )

        bucket.append(now)
        return await call_next(request)
