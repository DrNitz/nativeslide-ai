"""
NativeSlide AI — LLM Orchestration Service
Uses Google Gemini 1.5 Flash (free tier) to convert raw text/topics
into fully structured slide JSON specifications following the DeckSpec schema.
"""
from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any

from app.core.config import get_settings
from app.engine.themes import detect_theme
from app.models.schemas import (
    CardItem,
    DeckSpec,
    MetricItem,
    SlideLayout,
    SlideSpec,
    TableData,
    ThemeMood,
)

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai  # type: ignore
    _HAS_GEMINI = True
except ImportError:
    _HAS_GEMINI = False


class LLMService:
    """Orchestrates Gemini 1.5 Flash API calls to plan and structure presentations."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._client_ready = False

        if _HAS_GEMINI and self.settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=self.settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(self.settings.GEMINI_MODEL)
                self._client_ready = True
            except Exception as e:
                logger.warning(f"Could not initialize Gemini client: {e}")

    def _build_system_prompt(self, num_slides: int, theme_mood: ThemeMood) -> str:
        return f"""You are an elite executive presentation designer and domain consultant.
Your job is to transform raw input text or a topic into a cohesive, publication-grade {num_slides}-slide presentation.

CRITICAL STRUCTURAL RULES:
1. Every slide must use one of these exact layout keys:
   - "TITLE_HERO": Slide 1 only. Title, subtitle, kicker, date/author.
   - "METRICS_CALLOUT": 3 prominent headline numbers/metrics with short labels and explanations.
   - "CARDS_3X2": 4 to 6 structured concept cards arranged in a grid with bold lead-ins.
   - "TABLE_MATRIX": Rich comparison table with 3-5 headers and 3-6 rows of deep data.
   - "CASE_SCENARIOS": 3 to 5 realistic personas, clinical cases, or real-world application examples.
   - "COMPARISON_2COL": Side-by-side comparison (Before vs After, Pros vs Cons, Urgency vs Emergency).
   - "PROCESS_STEPS": Sequential workflow or protocol with 4-5 numbered milestones.
   - "SECTION_DIVIDER": Major module or domain transition slide.

2. CONTENT DENSITY & TONE:
   - Write professional, dense, executive-level content with real facts, numbers, and mechanisms.
   - Avoid generic fluff like "Innovation is important". Provide specific technical or clinical depth.
   - Every slide MUST include comprehensive, 3 to 5 sentence speaker notes explaining the reasoning, background evidence, and delivery advice.

3. OUTPUT FORMAT:
   - Respond ONLY with valid, raw JSON matching this schema exactly.
   - Do NOT wrap in markdown code fences like ```json ... ```. Output raw JSON only.

JSON SCHEMA EXPECTED:
{{
  "title": "Presentation Title",
  "theme_mood": "{theme_mood.value}",
  "total_slides": {num_slides},
  "slides": [
    {{
      "slide_number": 1,
      "layout": "TITLE_HERO",
      "title": "Main Presentation Title",
      "kicker": "Domain or Category",
      "body_text": "Executive Subtitle / Target Audience",
      "speaker_notes": "Opening remarks, setting the agenda, framing the problem."
    }},
    {{
      "slide_number": 2,
      "layout": "METRICS_CALLOUT",
      "title": "Key Landscape Metrics",
      "kicker": "Context & Scale",
      "metrics": [
        {{"value": "1.2B", "label": "Global Market Size", "description": "Rapidly growing addressable audience."}},
        {{"value": "48%", "label": "Adoption Rate", "description": "Year-over-year expansion in target segment."}},
        {{"value": "3.5x", "label": "Performance Multiple", "description": "Efficiency advantage over baseline."}}
      ],
      "speaker_notes": "Deep speaker notes explaining each metric."
    }}
  ]
}}
"""

    async def plan_deck(
        self,
        topic: str,
        content: str,
        num_slides: int,
        theme_override: ThemeMood | None = None,
    ) -> DeckSpec:
        """
        Generate a fully structured DeckSpec using Gemini 1.5 Flash.
        Falls back to a structured deterministic outline if API is unconfigured.
        """
        theme_mood = theme_override or detect_theme(topic, content[:500])

        if self._client_ready:
            try:
                prompt = self._build_system_prompt(num_slides, theme_mood)
                user_msg = f"TOPIC: {topic}\n\nCONTENT / REFERENCE MATERIAL:\n{content[:20000]}"

                response = self.model.generate_content(
                    f"{prompt}\n\n{user_msg}",
                    generation_config={"temperature": 0.3, "max_output_tokens": 8192},
                )
                text_resp = response.text.strip()
                # Clean any markdown fences if present
                text_resp = re.sub(r"^```(?:json)?\s*", "", text_resp)
                text_resp = re.sub(r"\s*```$", "", text_resp)

                data = json.loads(text_resp)
                return DeckSpec.model_validate(data)
            except Exception as exc:
                logger.error(f"Gemini generation error: {exc}. Using robust fallback generator.")

        # Fallback generator for offline/dev/demo testing
        return self._generate_fallback_deck(topic, content, num_slides, theme_mood)

    def _generate_fallback_deck(
        self,
        topic: str,
        content: str,
        num_slides: int,
        theme_mood: ThemeMood,
    ) -> DeckSpec:
        """Deterministic high-quality fallback generator when LLM API key is not present."""
        clean_title = topic.strip().title() if topic else "Executive Briefing"
        slides: list[SlideSpec] = []

        # Slide 1: Title
        slides.append(
            SlideSpec(
                slide_number=1,
                layout=SlideLayout.TITLE_HERO,
                title=clean_title,
                kicker="Executive Masterclass & Analysis",
                body_text="Comprehensive Overview, Core Principles & Strategic Implementations",
                speaker_notes=f"Welcome everyone. Today we are doing a deep dive into {clean_title}. We will cover foundations, quantitative benchmarks, key comparisons, and practical applications.",
            )
        )

        # Slide 2: Metrics Callout
        slides.append(
            SlideSpec(
                slide_number=2,
                layout=SlideLayout.METRICS_CALLOUT,
                title="Foundational Metrics & Global Scope",
                kicker="Key Landscape Statistics",
                metrics=[
                    MetricItem(
                        value="85%",
                        label="Domain Adoption",
                        description="Proportion of organizations accelerating implementation in current cycle.",
                    ),
                    MetricItem(
                        value="3.2x",
                        label="Efficiency Multiple",
                        description="Demonstrated improvement across controlled benchmark evaluations.",
                    ),
                    MetricItem(
                        value="<24h",
                        label="Turnaround Velocity",
                        description="Standard operational latency reduction achieved in pilot cohorts.",
                    ),
                ],
                speaker_notes="These three figures anchor our understanding of the scope and leverage points in this domain. Focus on the 3.2x efficiency multiple as our primary north star.",
            )
        )

        # Slide 3: 3x2 Cards
        slides.append(
            SlideSpec(
                slide_number=3,
                layout=SlideLayout.CARDS_3X2,
                title="Core Architectural Pillars",
                kicker="Foundations & Principles",
                cards=[
                    CardItem(title="Pillar 1: Structural Integrity", subtitle="Baseline Protocol", body="Establishes deterministic boundaries, ensuring uniform consistency across execution units."),
                    CardItem(title="Pillar 2: Dynamic Agility", subtitle="Adaptive Feedback", body="Incorporates closed-loop feedback mechanisms to recalibrate parameters dynamically."),
                    CardItem(title="Pillar 3: Scalable Throughput", subtitle="Parallel Processing", body="Decouples compute-heavy tasks to allow simultaneous multi-threaded execution."),
                    CardItem(title="Pillar 4: Safety & Verification", subtitle="Audit Framework", body="Implements multi-stage validation gates to prevent drift or unauthorized deviations."),
                    CardItem(title="Pillar 5: Resource Optimization", subtitle="Cost Efficiency", body="Minimizes redundant overhead while maximizing compute density per dollar invested."),
                    CardItem(title="Pillar 6: Sustainable Longevity", subtitle="Long-Term Horizon", body="Ensures backwards compatibility and maintainability across multi-year cycles."),
                ],
                speaker_notes="Walk the audience through each pillar in clockwise sequence, highlighting that Pillar 1 and Pillar 4 form the essential bedrock before scaling Pillar 3.",
            )
        )

        # Slide 4: Table Matrix
        slides.append(
            SlideSpec(
                slide_number=4,
                layout=SlideLayout.TABLE_MATRIX,
                title="Comparative Framework & Matrix Analysis",
                kicker="System Comparison",
                table=TableData(
                    headers=["PARADIGM", "CORE MECHANISM", "ADVANTAGES", "TRADE-OFFS", "OPTIMAL SCENARIO"],
                    rows=[
                        ["Standard Model", "Linear sequential execution", "High predictability, minimal edge cases", "Higher latency, resource underutilization", "Baseline legacy operations"],
                        ["Accelerated Matrix", "Vectorized parallel batching", "3x throughput, lower marginal cost", "Requires strict schema validation", "Production scale deployment"],
                        ["Dynamic Adaptive", "Heuristic-driven self-tuning", "Autonomous optimization over time", "Non-deterministic parameter shifts", "Research & exploratory domains"],
                        ["Hybrid Enterprise", "Dual-stage validation pipeline", "Combines speed with ironclad safety", "Slightly higher configuration complexity", "Mission-critical infrastructure"],
                    ],
                ),
                speaker_notes="This comparison matrix crystallizes the trade-offs between linear legacy approaches and modern accelerated matrix workflows. Note the hybrid enterprise model balance.",
            )
        )

        # Slide 5: Comparison 2-Column
        slides.append(
            SlideSpec(
                slide_number=5,
                layout=SlideLayout.COMPARISON_2COL,
                title="Strategic Trade-Offs: Conventional vs Modern",
                kicker="Paradigm Shift",
                cards=[
                    CardItem(
                        title="CONVENTIONAL METHODOLOGY",
                        subtitle="Manual, Fragmented, Low-Leverage",
                        body="• Relies heavily on ad-hoc intervention and manual formatting.\n• High error rates during high-velocity turnaround requirements.\n• Poor cross-functional alignment and difficult version control.\n• Non-reusable artifacts that degrade in utility over time.",
                    ),
                    CardItem(
                        title="MODERN VECTOR ARCHITECTURE",
                        subtitle="Automated, Deterministic, Scalable",
                        body="• Pure programmatic rendering with zero loss of fidelity.\n• Standardized design systems ensuring 100% brand coherence.\n• Rapid turnaround with instant downloadable native output.\n• High-leverage execution delivering outsized competitive advantages.",
                    ),
                ],
                speaker_notes="Here we juxtapose the two paradigms side by side. Highlight that moving from left to right unlocks non-linear gains in operational velocity.",
            )
        )

        # Fill remaining requested slides up to num_slides
        curr = len(slides) + 1
        while curr <= num_slides:
            slides.append(
                SlideSpec(
                    slide_number=curr,
                    layout=SlideLayout.CARDS_3X2 if curr % 2 == 0 else SlideLayout.METRICS_CALLOUT,
                    title=f"Implementation Phase {curr - 4}: Strategic Deep Dive",
                    kicker=f"Module {curr - 4}",
                    cards=[
                        CardItem(title="Milestone A", subtitle="Phase Initiation", body="Establish clear baseline metrics and allocate dedicated operational resources."),
                        CardItem(title="Milestone B", subtitle="Execution Sprint", body="Deploy targeted interventions and monitor telemetry continuously for variance."),
                        CardItem(title="Milestone C", subtitle="Validation Gate", body="Verify output quality against rigorous predefined acceptance thresholds."),
                    ] if curr % 2 == 0 else None,
                    metrics=[
                        MetricItem(value=f"{curr * 10}%", label="Completion Index", description="Target readiness metric for this milestone."),
                        MetricItem(value="Zero", label="Tolerance for Error", description="Deterministic quality gates enforced."),
                        MetricItem(value="24/7", label="Operational Uptime", description="Continuous service availability."),
                    ] if curr % 2 != 0 else None,
                    speaker_notes=f"This slide covers Phase {curr - 4} of our roadmap. Reiterate accountability and the key performance indicators listed.",
                )
            )
            curr += 1

        return DeckSpec(
            title=clean_title,
            total_slides=len(slides),
            theme_mood=theme_mood,
            slides=slides,
            generated_at=datetime.now(timezone.utc),
        )
