"""
NativeSlide AI — Generation API Endpoints
POST /api/generate/from-topic
POST /api/generate/from-pdf
GET  /api/generate/status/{job_id}
GET  /api/generate/download/{job_id}
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.config import get_settings
from app.engine.builder import DeckBuilder
from app.engine.themes import THEME_REGISTRY, ThemeMood, detect_theme
from app.models.schemas import GenerationRequest, GenerationResponse, ThemeMood
from app.services.llm_service import LLMService
from app.services.pdf_service import PDFService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/generate", tags=["generation"])
settings = get_settings()

llm_service = LLMService()
pdf_service = PDFService()

# In-memory job repository (replace with Supabase/Redis in production)
JOBS: dict[str, dict] = {}


@router.post("/from-topic", response_model=GenerationResponse)
async def generate_from_topic(payload: GenerationRequest) -> GenerationResponse:
    """
    Generate an executive presentation directly from a topic prompt or pasted notes.
    """
    if not payload.topic and not payload.content_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'topic' or 'content_text' must be provided.",
        )

    job_id = str(uuid4())
    topic = payload.topic or "Executive Presentation"
    content = payload.content_text or payload.topic or ""
    num_slides = min(payload.num_slides, settings.FREE_TIER_MAX_SLIDES)

    now = datetime.now(timezone.utc)
    expires = now + timedelta(hours=48)

    # Detect or override theme
    theme_mood = payload.theme_override or detect_theme(topic, content[:500])
    theme_colors = THEME_REGISTRY[theme_mood]

    try:
        # Step 1: LLM plans the slides
        deck_spec = await llm_service.plan_deck(
            topic=topic,
            content=content,
            num_slides=num_slides,
            theme_override=theme_mood,
        )

        # Step 2: Builder renders native DrawingML PPTX
        builder = DeckBuilder(spec=deck_spec, theme=theme_colors)
        output_path = builder.build()

        JOBS[job_id] = {
            "job_id": job_id,
            "status": "completed",
            "file_path": str(output_path),
            "title": deck_spec.title,
            "slide_count": len(deck_spec.slides),
            "theme_used": theme_mood.value,
            "created_at": now,
            "expires_at": expires,
        }

        return GenerationResponse(
            job_id=job_id,
            status="completed",
            download_url=f"/api/generate/download/{job_id}",
            slide_count=len(deck_spec.slides),
            theme_used=theme_mood,
            created_at=now,
            expires_at=expires,
        )

    except Exception as exc:
        logger.error(f"Deck generation failed for job {job_id}: {exc}", exc_info=True)
        JOBS[job_id] = {
            "job_id": job_id,
            "status": "failed",
            "error": str(exc),
            "created_at": now,
            "expires_at": expires,
        }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {exc}",
        )


@router.post("/from-pdf", response_model=GenerationResponse)
async def generate_from_pdf(
    file: UploadFile = File(...),
    user_id: str = Form("anonymous"),
    num_slides: int = Form(15),
    theme_override: str | None = Form(None),
) -> GenerationResponse:
    """
    Extract text from an uploaded PDF and transform it into an executive presentation.
    """
    extracted_text = await pdf_service.validate_and_extract(file)

    # Use filename as topic hint
    topic_hint = file.filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ")

    theme_enum = None
    if theme_override:
        try:
            theme_enum = ThemeMood(theme_override)
        except ValueError:
            pass

    req = GenerationRequest(
        topic=topic_hint,
        content_text=extracted_text,
        num_slides=num_slides,
        theme_override=theme_enum,
        user_id=user_id,
    )
    return await generate_from_topic(req)


@router.get("/status/{job_id}")
async def get_job_status(job_id: str) -> dict:
    """Check the processing status of a generation job."""
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found.",
        )
    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "slide_count": job.get("slide_count"),
        "theme_used": job.get("theme_used"),
        "created_at": job["created_at"],
        "expires_at": job["expires_at"],
        "download_url": f"/api/generate/download/{job_id}" if job["status"] == "completed" else None,
    }


@router.get("/download/{job_id}")
async def download_deck(job_id: str) -> FileResponse:
    """Download the generated .pptx presentation file."""
    job = JOBS.get(job_id)
    if not job or job.get("status") != "completed":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found or not yet ready.",
        )

    file_path = Path(job["file_path"])
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Presentation file has expired or was removed.",
        )

    clean_filename = f"{job.get('title', 'presentation')[:40].replace(' ', '_')}.pptx"

    return FileResponse(
        path=str(file_path),
        filename=clean_filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
