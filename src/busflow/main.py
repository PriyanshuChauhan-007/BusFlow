import asyncio
import logging
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from busflow.config import get_settings
from busflow.health import check_postgres, check_redis
from busflow.logging_config import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)
    app.state.settings = settings
    app.state.redis = Redis.from_url(settings.redis_url, decode_responses=True)
    app.state.postgres_factory = lambda: asyncpg.connect(settings.database_url)
    logger.info("busflow_api_started")
    try:
        yield
    finally:
        await app.state.redis.aclose()
        logger.info("busflow_api_stopped")


app = FastAPI(
    title="BusFlow API",
    version="0.1.0",
    description="Real-time transit tracking and ETA platform API.",
    lifespan=lifespan,
)


@app.get("/health/live", tags=["health"])
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
async def readiness(request: Request):
    postgres_ready, redis_ready = await asyncio.gather(
        check_postgres(request.app.state.postgres_factory),
        check_redis(request.app.state.redis),
    )
    dependencies = {"postgres": postgres_ready, "redis": redis_ready}
    ready = all(dependencies.values())
    body = {"status": "ok" if ready else "not_ready", "dependencies": dependencies}
    if not ready:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=body)
    return body
