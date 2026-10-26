"""
NativeSlide AI — Main Application Entry Point
FastAPI service exposing generation routes, health checks, and OpenAPI docs.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.generate import router as generate_router
from app.core.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("nativeslide")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure output directory exists
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"NativeSlide AI starting up. Output directory: {settings.OUTPUT_DIR}")
    yield
    # Shutdown
    logger.info("NativeSlide AI shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Turn any PDF, paper, or topic into a 100% editable, native DrawingML PowerPoint presentation.",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware for Next.js frontend on Cloudflare Pages or localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(generate_router)


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """System health check and engine capability verification."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "engine": "DrawingML OpenXML Vector Engine v1",
        "llm_model": settings.GEMINI_MODEL,
        "free_tier_max_slides": settings.FREE_TIER_MAX_SLIDES,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
