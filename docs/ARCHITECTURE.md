# NativeSlide AI — System Architecture & Technical Specifications

> **Turn any PDF, paper, or topic into a 100% editable, native DrawingML PowerPoint deck in 30 seconds.**

---

## 1. System Overview

NativeSlide AI decouples presentation generation from proprietary web players or flat raster image exports. Every deck generated consists of **100% native DrawingML vector shapes, text frames, and OpenXML tables** that render cleanly in Microsoft PowerPoint (desktop/web), Apple Keynote, and Google Slides.

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT LAYER                          │
│   Next.js 14 (App Router) + Tailwind CSS + TypeScript       │
│   Hosted on Cloudflare Pages (Free Tier: Unlimited Egress)  │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / JSON / FormData
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       BACKEND API                           │
│   FastAPI Python 3.11+ Service                              │
│   Hosted on Oracle Cloud Always Free (4 ARM Cores, 24GB RAM)│
│                                                             │
│   ┌───────────────────┐    ┌────────────────────────────┐   │
│   │   PDF Service     │    │       LLM Service          │   │
│   │ (pdfplumber/pypdf)│    │ (Gemini 1.5 Flash Free API)│   │
│   └─────────┬─────────┘    └─────────────┬──────────────┘   │
│             │                            │                  │
│             └──────────────┬─────────────┘                  │
│                            ▼                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │            DrawingML Engine (DeckBuilder)           │   │
│   │     python-pptx + vector_kit + dynamic palettes     │   │
│   └────────────────────────┬────────────────────────────┘   │
└────────────────────────────┼────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                 PERSISTENCE & AUTHENTICATION                │
│   Supabase (PostgreSQL + Google OAuth)                      │
│   - Free Tier: 50,000 MAUs                                  │
│   - Tracks 48-Hour Trial Window & Deck Credits              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. The DrawingML Advantage vs Competitors

Most existing AI presentation makers (Gamma, Tome, SlidesAI, Beautiful.ai) have structural limitations:
1. **Proprietary Player Lock-in:** Presentations only live on their custom web apps.
2. **Flat Raster Exports:** Exporting to `.pptx` converts cards and graphics into flat 72 DPI PNG/JPEG screenshots. Users cannot change a single number, re-color a pill, or resize a column in PowerPoint.
3. **Broken Text Formatting:** When fonts aren't installed, layouts break and overflow.

**NativeSlide AI Output Quality:**
* **100% Native Shapes:** Every card is an OpenXML `<p:sp>` with real border radius adjustments and native drop-shadow filters.
* **Native Tables:** Renders real DrawingML `<a:tbl>` elements with uniform cell margins, alternating fills, and dynamic column proportions.
* **Deep Speaker Notes:** Embeds rich 3–5 sentence clinical/executive presenter notes into `<p:notesSlide>` for every single slide.
* **Zero Embedded Raster Bitmaps:** The entire 30+ slide `.pptx` file is typically under **250 KB** in file size.

---

## 3. Dynamic Chameleon Theme Palettes

The engine applies the **60-30-10 Color Rule** across 8 distinct domain themes:

| Theme Mood | Background (60%) | Header / Text (30%) | Primary Accent (10%) | Secondary Accent | Target Domain |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`MEDICINE_CLINICAL`** | `#F8FAFC` (Slate 50) | `#0B192C` (Deep Navy) | `#00A896` (Clinical Teal) | `#E11D48` (Rose) | Healthcare, Harrison's, Pharma, Cardiology |
| **`SPACE_ASTRONOMY`** | `#060B18` (Cosmic Black) | `#E2E8F0` (Starlight Silver)| `#00E5FF` (Electric Cyan)| `#8B5CF6` (Nebula Purple)| Astrophysics, Space Missions, Quantum |
| **`AI_ML_TECH`** | `#0F172A` (Cyber Slate) | `#F1F5F9` (Ice White) | `#10B981` (Neon Emerald) | `#6366F1` (Laser Indigo)| Machine Learning, LLMs, Developer Tools |
| **`LAW_JUDICIARY`** | `#FAFAF7` (Warm Cream) | `#1C1917` (Charcoal) | `#881337` (Burgundy) | `#D97706` (Antique Gold)| Contracts, Case Law, Statutory Analysis |
| **`ARCHITECTURE_DESIGN`**| `#FFFFFF` (Pure White) | `#111111` (Matte Black) | `#C2410C` (Terracotta) | `#64748B` (Concrete) | Urbanism, Architecture, Industrial Design |
| **`FINANCE_BUSINESS`** | `#F8FAFC` (Cloud White) | `#0A192F` (Wall St Navy)| `#1D4ED8` (Royal Blue) | `#0D9488` (Growth Teal) | Earnings, PE/VC Pitch Decks, Valuation |
| **`EDUCATION_ACADEMIC`**| `#FFFBF5` (Ivory Paper) | `#1E3A5F` (Oxford Navy) | `#2563EB` (Cobalt) | `#7C3AED` (Violet) | Lectures, Curriculums, Textbooks |
| **`ENGINEERING_TECHNICAL`**| `#F8FAFC` (Clean White) | `#0F172A` (Carbon) | `#0EA5E9` (Sky Blue) | `#F97316` (Safety Orange)| Mechanical, Civil, Systems Architecture |

---

## 4. Database Schema (Supabase PostgreSQL)

```sql
-- Users & Credit Tracking
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    full_name TEXT,
    free_credits_remaining INT DEFAULT 1,
    trial_started_at TIMESTAMPTZ DEFAULT NOW(),
    trial_expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '48 hours'),
    is_pro BOOLEAN DEFAULT FALSE,
    pro_expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated Decks
CREATE TABLE public.decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    topic TEXT,
    num_slides INT NOT NULL,
    theme_mood TEXT NOT NULL,
    storage_path TEXT,
    file_size_bytes BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '48 hours')
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.decks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users view own decks" ON public.decks FOR SELECT USING (auth.uid() = user_id);
```

---

## 5. Zero-Cost Economics Breakdown

| Tier | Provider | Free Allocation | Commercial Value | Cost to Operator |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend CDN** | Cloudflare Pages | Unlimited Bandwidth, 500 builds/mo | $20/mo equivalent | **$0.00** |
| **Compute Server** | Oracle Cloud Always Free | 4 Ampere ARM Cores, 24GB RAM, 200GB disk | $80/mo equivalent | **$0.00** |
| **Database & Auth** | Supabase Free | 50,000 Monthly Active Users, 500MB DB | $25/mo equivalent | **$0.00** |
| **AI LLM API** | Google AI Studio (Gemini 1.5 Flash)| 15 RPM, 1,500 Requests Per Day | $150/mo equivalent | **$0.00** |
| **TOTAL** | | | | **$0.00 / month** |
