import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 

from app.config import settings
from app.presentation.api import router


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    This is a lifespan context manager for FastAPI that handles application startup and shutdown events.
    What it does:

    Startup (code before yield) — Runs once when your FastAPI app starts. This is where you initialize resources like:

    Loading ML models into memory
    Establishing database connection pools
    Warming up caches


    yield — The app runs and handles requests during this time
    Shutdown (code after yield) — Runs once when the app stops. Used for cleanup like:

    Releasing model memory
    Closing database connections
    Flushing logs
    """
    logger.info("Starting Gymnius API", environment=settings.environment)
    # TODO: Load ML models here
    yield
    logger.info("Shutting down Gymnius API")

    
app = FastAPI(
    title=settings.app_name,
    description="Food recognition for calorie counting",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware('http')
async def timing_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = str(round(duration_ms, 2))

    logger.info(
        "request_completed",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=round(duration_ms, 2),
    )

    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", error=str(exc))
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return JSONResponse(status_code=200, content = {"message": "Gymnius-V2 API is live"})

