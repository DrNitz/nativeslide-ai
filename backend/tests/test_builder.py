"""
NativeSlide AI — Test Suite
Validates schema validation, theme detection, and DrawingML deck generation.
"""
from pathlib import Path
from app.models.schemas import ThemeMood
from app.engine.themes import THEME_REGISTRY, detect_theme
from app.services.llm_service import LLMService
from app.engine.builder import DeckBuilder


def test_theme_registry():
    assert len(THEME_REGISTRY) == 8
    assert ThemeMood.MEDICINE_CLINICAL in THEME_REGISTRY
    assert THEME_REGISTRY[ThemeMood.MEDICINE_CLINICAL].accent_primary == "00A896"


def test_detect_theme():
    assert detect_theme("Hypertension Clinical Management", "") == ThemeMood.MEDICINE_CLINICAL
    assert detect_theme("Deep Space Telescopes and Galaxies", "") == ThemeMood.SPACE_ASTRONOMY
    assert detect_theme("Deep Neural Networks and Transformer Weights", "") == ThemeMood.AI_ML_TECH
    assert detect_theme("Constitutional Statutory Precedent", "") == ThemeMood.LAW_JUDICIARY


def test_builder_fallback_deck():
    llm = LLMService()
    spec = llm._generate_fallback_deck(
        topic="Test Architectural Blueprints",
        content="",
        num_slides=5,
        theme_mood=ThemeMood.ARCHITECTURE_DESIGN,
    )
    assert len(spec.slides) == 5
    assert spec.title == "Test Architectural Blueprints"

    theme = THEME_REGISTRY[spec.theme_mood]
    builder = DeckBuilder(spec=spec, theme=theme)
    output_path = builder.build()

    assert Path(output_path).exists()
    assert Path(output_path).stat().st_size > 1000
