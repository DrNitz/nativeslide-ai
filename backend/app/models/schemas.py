"""
NativeSlide AI — Pydantic v2 Data Models & Schemas
Shared data contracts used by the API layer, LLM service, and PPTX engine.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ── Enums ─────────────────────────────────────────────────────────────────────

class SlideLayout(str, Enum):
    """Supported slide layout templates rendered by the DrawingML engine."""
    TABLE_MATRIX = "TABLE_MATRIX"
    CARDS_3X2 = "CARDS_3X2"
    CASE_SCENARIOS = "CASE_SCENARIOS"
    METRICS_CALLOUT = "METRICS_CALLOUT"
    COMPARISON_2COL = "COMPARISON_2COL"
    PROCESS_STEPS = "PROCESS_STEPS"
    TITLE_HERO = "TITLE_HERO"
    SECTION_DIVIDER = "SECTION_DIVIDER"


class ThemeMood(str, Enum):
    """Visual theme moods — each maps to a full palette in the theme registry."""
    MEDICINE_CLINICAL = "MEDICINE_CLINICAL"
    SPACE_ASTRONOMY = "SPACE_ASTRONOMY"
    AI_ML_TECH = "AI_ML_TECH"
    LAW_JUDICIARY = "LAW_JUDICIARY"
    ARCHITECTURE_DESIGN = "ARCHITECTURE_DESIGN"
    FINANCE_BUSINESS = "FINANCE_BUSINESS"
    EDUCATION_ACADEMIC = "EDUCATION_ACADEMIC"
    ENGINEERING_TECHNICAL = "ENGINEERING_TECHNICAL"


# ── Slide Content Primitives ──────────────────────────────────────────────────

class MetricItem(BaseModel):
    """A single highlighted metric for METRICS_CALLOUT slides."""
    value: str = Field(..., description="The headline figure, e.g. '87%' or '2.4B'.")
    label: str = Field(..., description="Short label under the value, e.g. 'Accuracy'.")
    description: str = Field(..., description="One-sentence elaboration shown below the label.")
    accent_color: str | None = Field(
        default=None,
        description="Optional hex color override for this metric card accent.",
    )


class CardItem(BaseModel):
    """A content card for CARDS_3X2 or CASE_SCENARIOS layouts."""
    title: str = Field(..., description="Card headline text.")
    subtitle: str | None = Field(default=None, description="Optional sub-heading.")
    body: str = Field(..., description="Card body paragraph text.")
    accent_color: str | None = Field(
        default=None,
        description="Optional hex color for the card top-accent bar.",
    )


class TableData(BaseModel):
    """Structured data for TABLE_MATRIX slides rendered as native <a:tbl>."""
    headers: list[str] = Field(..., description="Column header labels.")
    rows: list[list[str]] = Field(..., description="Table data rows (list of row lists).")
    column_widths: list[float] | None = Field(
        default=None,
        description="Optional relative column width fractions (must sum to 1.0).",
    )


# ── Slide & Deck Specs ────────────────────────────────────────────────────────

class SlideSpec(BaseModel):
    """Complete specification for a single slide, consumed by DeckBuilder."""
    slide_number: int = Field(..., ge=1, description="1-based slide index.")
    layout: SlideLayout = Field(..., description="DrawingML layout template to render.")
    title: str = Field(..., description="Main slide title text.")
    kicker: str | None = Field(
        default=None,
        description="Small label shown above the title (section tag, chapter name).",
    )
    metrics: list[MetricItem] | None = Field(
        default=None,
        description="Metric items for METRICS_CALLOUT layout (max 3).",
    )
    cards: list[CardItem] | None = Field(
        default=None,
        description="Card items for CARDS_3X2 or COMPARISON_2COL layouts.",
    )
    table: TableData | None = Field(
        default=None,
        description="Table data for TABLE_MATRIX layout.",
    )
    body_text: str | None = Field(
        default=None,
        description="Freeform body text for TITLE_HERO, SECTION_DIVIDER, PROCESS_STEPS.",
    )
    speaker_notes: str = Field(
        ...,
        min_length=1,
        description="Publication-grade presenter notes (minimum 3–4 sentences).",
    )


class DeckSpec(BaseModel):
    """Full deck specification: metadata + ordered list of SlideSpecs."""
    title: str = Field(..., description="Deck title used as the first slide headline.")
    total_slides: int = Field(..., ge=1, description="Total number of slides in this deck.")
    theme_mood: ThemeMood = Field(..., description="Visual theme palette applied globally.")
    slides: list[SlideSpec] = Field(..., description="Ordered list of slide specifications.")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of when this spec was generated.",
    )


# ── API Request / Response Models ─────────────────────────────────────────────

class GenerationRequest(BaseModel):
    """Request body for POST /api/generate/from-topic."""
    topic: str | None = Field(
        default=None,
        description="Short topic string, e.g. 'Hypertension management per Harrison's'.",
    )
    content_text: str | None = Field(
        default=None,
        description="Raw pasted content to use as the source material.",
    )
    num_slides: int = Field(
        default=15,
        ge=5,
        le=40,
        description="Desired number of slides in the output deck.",
    )
    theme_override: ThemeMood | None = Field(
        default=None,
        description="Force a specific theme instead of auto-detecting from content.",
    )
    user_id: str = Field(..., description="Authenticated user UUID from Supabase.")


class GenerationResponse(BaseModel):
    """Response returned immediately after a generation job is enqueued."""
    job_id: str = Field(..., description="Unique job identifier for status polling.")
    status: str = Field(..., description="Current job status: queued | processing | done | error.")
    download_url: str | None = Field(
        default=None,
        description="Signed download URL for the .pptx file (available when status=done).",
    )
    slide_count: int | None = Field(
        default=None,
        description="Final number of slides rendered (available when status=done).",
    )
    theme_used: ThemeMood | None = Field(
        default=None,
        description="Theme palette applied to the generated deck.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the job was created.",
    )
    expires_at: datetime = Field(
        ...,
        description="UTC timestamp when the generated file will be deleted from storage.",
    )


# ── User / Credits Models ─────────────────────────────────────────────────────

class UserCredits(BaseModel):
    """User subscription and credit state."""
    user_id: str = Field(..., description="Supabase user UUID.")
    free_credits_remaining: int = Field(
        ...,
        ge=0,
        description="Number of free deck generations remaining this billing period.",
    )
    is_pro: bool = Field(
        default=False,
        description="Whether the user has an active Pro subscription.",
    )
    pro_expires_at: datetime | None = Field(
        default=None,
        description="UTC expiry of Pro subscription (None if not Pro).",
    )
