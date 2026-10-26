"""
NativeSlide AI — Dynamic Theme Palette System
Maps ThemeMood enum values to fully specified ThemeColors palettes.
All colors are hex strings (without leading #) for compatibility with
python-pptx RGBColor construction.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from app.models.schemas import ThemeMood


@dataclass
class ThemeColors:
    """
    Complete color palette for a single theme mood.
    All hex values are 6-character strings WITHOUT the leading '#'.
    """
    # Slide background tones
    background_primary: str
    background_secondary: str
    header_bg: str

    # Brand accent hierarchy
    accent_primary: str
    accent_secondary: str
    accent_tertiary: str

    # Text scale
    text_dark: str
    text_medium: str
    text_light: str

    # Card / table surface colors
    card_fill: str
    card_border: str
    table_header_bg: str
    table_row_alt: str

    # Constants
    white: str = field(default="FFFFFF")
    font_primary: str = field(default="Inter")


# ── Theme Registry ────────────────────────────────────────────────────────────

THEME_REGISTRY: dict[ThemeMood, ThemeColors] = {

    ThemeMood.MEDICINE_CLINICAL: ThemeColors(
        background_primary="F8FAFC",
        background_secondary="EFF6FF",
        header_bg="0B192C",
        accent_primary="00A896",
        accent_secondary="E11D48",
        accent_tertiary="F59E0B",
        text_dark="0B192C",
        text_medium="374151",
        text_light="6B7280",
        card_fill="FFFFFF",
        card_border="E2E8F0",
        table_header_bg="0B192C",
        table_row_alt="F0F9FF",
    ),

    ThemeMood.SPACE_ASTRONOMY: ThemeColors(
        background_primary="060B18",
        background_secondary="0A1628",
        header_bg="0A1628",
        accent_primary="00E5FF",
        accent_secondary="8B5CF6",
        accent_tertiary="F59E0B",
        text_dark="E2E8F0",
        text_medium="94A3B8",
        text_light="64748B",
        card_fill="0D1F3C",
        card_border="1E3A5F",
        table_header_bg="0D1F3C",
        table_row_alt="060B18",
        font_primary="Inter",
    ),

    ThemeMood.AI_ML_TECH: ThemeColors(
        background_primary="0F172A",
        background_secondary="1E293B",
        header_bg="1E293B",
        accent_primary="10B981",
        accent_secondary="6366F1",
        accent_tertiary="F59E0B",
        text_dark="F1F5F9",
        text_medium="CBD5E1",
        text_light="94A3B8",
        card_fill="1E293B",
        card_border="334155",
        table_header_bg="1E293B",
        table_row_alt="0F172A",
        font_primary="Inter",
    ),

    ThemeMood.LAW_JUDICIARY: ThemeColors(
        background_primary="FAFAF7",
        background_secondary="F5F5F0",
        header_bg="1C1917",
        accent_primary="881337",
        accent_secondary="D97706",
        accent_tertiary="1C1917",
        text_dark="1C1917",
        text_medium="44403C",
        text_light="78716C",
        card_fill="FFFFFF",
        card_border="E7E5E4",
        table_header_bg="1C1917",
        table_row_alt="FAF9F6",
        font_primary="Georgia",
    ),

    ThemeMood.ARCHITECTURE_DESIGN: ThemeColors(
        background_primary="FFFFFF",
        background_secondary="F9FAFB",
        header_bg="111111",
        accent_primary="C2410C",
        accent_secondary="64748B",
        accent_tertiary="0EA5E9",
        text_dark="111111",
        text_medium="374151",
        text_light="9CA3AF",
        card_fill="FAFAFA",
        card_border="E5E7EB",
        table_header_bg="111111",
        table_row_alt="F9FAFB",
        font_primary="Inter",
    ),

    ThemeMood.FINANCE_BUSINESS: ThemeColors(
        background_primary="F8FAFC",
        background_secondary="EFF6FF",
        header_bg="0A192F",
        accent_primary="1D4ED8",
        accent_secondary="0D9488",
        accent_tertiary="D97706",
        text_dark="0A192F",
        text_medium="1E40AF",
        text_light="6B7280",
        card_fill="FFFFFF",
        card_border="DBEAFE",
        table_header_bg="0A192F",
        table_row_alt="EFF6FF",
        font_primary="Inter",
    ),

    ThemeMood.EDUCATION_ACADEMIC: ThemeColors(
        background_primary="FFFBF5",
        background_secondary="FEF3C7",
        header_bg="1E3A5F",
        accent_primary="2563EB",
        accent_secondary="7C3AED",
        accent_tertiary="059669",
        text_dark="1E3A5F",
        text_medium="374151",
        text_light="6B7280",
        card_fill="FFFFFF",
        card_border="E5E7EB",
        table_header_bg="1E3A5F",
        table_row_alt="FFFBF5",
        font_primary="Inter",
    ),

    ThemeMood.ENGINEERING_TECHNICAL: ThemeColors(
        background_primary="F8FAFC",
        background_secondary="F0F9FF",
        header_bg="0F172A",
        accent_primary="0EA5E9",
        accent_secondary="F97316",
        accent_tertiary="8B5CF6",
        text_dark="0F172A",
        text_medium="334155",
        text_light="64748B",
        card_fill="FFFFFF",
        card_border="E2E8F0",
        table_header_bg="0F172A",
        table_row_alt="F0F9FF",
        font_primary="Inter",
    ),
}


# ── Theme Auto-Detection ──────────────────────────────────────────────────────

_KEYWORD_MAP: list[tuple[list[str], ThemeMood]] = [
    (
        ["medical", "medicine", "hypertension", "clinical", "drug", "patient",
         "diagnosis", "treatment", "symptom", "pharmacology", "hospital", "cardiac",
         "oncology", "radiology", "surgery", "physician", "dosage", "therapy"],
        ThemeMood.MEDICINE_CLINICAL,
    ),
    (
        ["space", "astronomy", "galaxy", "quantum", "nasa", "telescope", "cosmos",
         "orbit", "satellite", "astrophysics", "celestial", "nebula", "exoplanet",
         "gravitational", "black hole", "supernova", "cosmology"],
        ThemeMood.SPACE_ASTRONOMY,
    ),
    (
        ["ai", "artificial intelligence", "machine learning", "neural", "llm",
         "pytorch", "tensorflow", "transformer", "deep learning", "diffusion",
         "language model", "reinforcement learning", "computer vision", "nlp",
         "chatgpt", "gpt", "embedding", "inference", "fine-tuning"],
        ThemeMood.AI_ML_TECH,
    ),
    (
        ["law", "legal", "contract", "court", "statute", "regulation", "compliance",
         "litigation", "jurisdiction", "legislation", "attorney", "plaintiff",
         "defendant", "judicial", "precedent", "clause", "arbitration"],
        ThemeMood.LAW_JUDICIARY,
    ),
    (
        ["architecture", "design", "building", "structure", "urban", "construction",
         "blueprint", "facade", "interior", "spatial", "planning", "renovation",
         "landscape", "structural", "architectural", "typology"],
        ThemeMood.ARCHITECTURE_DESIGN,
    ),
    (
        ["finance", "stock", "revenue", "investment", "market", "financial",
         "portfolio", "equity", "valuation", "dividend", "roi", "hedge fund",
         "earnings", "quarterly", "balance sheet", "p&l", "fiscal", "budget",
         "economics", "macroeconomic", "inflation", "interest rate"],
        ThemeMood.FINANCE_BUSINESS,
    ),
    (
        ["engineering", "mechanical", "electrical", "circuit", "algorithm",
         "infrastructure", "network", "semiconductor", "embedded", "firmware",
         "pipeline", "protocol", "specification", "tolerance", "load testing"],
        ThemeMood.ENGINEERING_TECHNICAL,
    ),
]


def detect_theme(topic: str, content_preview: str = "") -> ThemeMood:
    """
    Auto-detect the best ThemeMood from a topic string and optional content preview.

    Applies a simple keyword-frequency scoring approach: the theme whose keyword
    list scores the most hits in the combined text wins. Falls back to
    EDUCATION_ACADEMIC when no keywords match.

    Args:
        topic: The user-supplied topic or document title.
        content_preview: First ~500 chars of extracted content (optional boost).

    Returns:
        The best-matching ThemeMood enum value.
    """
    combined = (topic + " " + content_preview).lower()

    best_mood = ThemeMood.EDUCATION_ACADEMIC
    best_score = 0

    for keywords, mood in _KEYWORD_MAP:
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_score:
            best_score = score
            best_mood = mood

    return best_mood
