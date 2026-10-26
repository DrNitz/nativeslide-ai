# NativeSlide AI

[![License: BUSL-1.1](https://img.shields.io/badge/License-BUSL--1.1-blue.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-brightgreen)](https://github.com/drnitz/nativeslide-ai)

> **Turn any PDF, paper, or topic into a 100% editable, native DrawingML PowerPoint deck in 30 seconds.**

---

## Why NativeSlide?

Most AI presentation tools export **flat raster images** embedded inside a `.pptx` container — you cannot edit a single shape, recolor a chart, or reflow a text box. NativeSlide AI is architecturally different.

| Feature | Gamma | Tome | SlidesAI | **NativeSlide AI** |
|---|---|---|---|---|
| Output format | Web embed | Web only | Raster PNG in PPTX | **100% native OpenXML DrawingML** |
| Shape editability | ❌ Locked | ❌ Web only | ❌ Flat image | ✅ **Every shape is a real vector** |
| Table cells | ❌ Image | ❌ Image | ❌ Image | ✅ **Native `<a:tbl>` table** |
| Speaker notes | Basic | None | None | ✅ **Publication-grade, 4+ sentences** |
| Offline editable | ❌ | ❌ | Partial | ✅ **Full PowerPoint editing** |
| Self-hostable | ❌ | ❌ | ❌ | ✅ **Oracle Always Free + Cloudflare** |
| Cost | $8–20/mo | $16/mo | $10/mo | ✅ **$0/mo (free tiers)** |

### The Key Differentiator

NativeSlide AI outputs presentations built entirely from `<p:sp>`, `<a:tbl>`, `<p:connector>`, and `<a:custGeom>` elements — the same primitives Microsoft PowerPoint itself writes. Every text box, metric card, table row, and icon is a fully editable native DrawingML vector object. Open the file in PowerPoint, Google Slides, or LibreOffice — everything is live and editable.

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        NativeSlide AI — System Architecture            │
└────────────────────────────────────────────────────────────────────────┘

  User Browser
      │
      ▼
┌─────────────────┐        HTTPS / REST API
│  Cloudflare     │ ──────────────────────────────────────►  ┌───────────────────────┐
│  Pages          │                                           │  Oracle Cloud         │
│  (Next.js 14    │ ◄──────────────────────────────────────  │  Always Free Instance │
│   Static Export)│        JSON + .pptx download             │  FastAPI + Uvicorn    │
└─────────────────┘                                          └──────────┬────────────┘
                                                                        │
                                              ┌─────────────────────────┼──────────────────────┐
                                              │                         │                      │
                                              ▼                         ▼                      ▼
                                   ┌──────────────────┐   ┌────────────────────┐  ┌───────────────────┐
                                   │  Google Gemini   │   │  python-pptx       │  │  Supabase         │
                                   │  1.5 Flash       │   │  DrawingML Engine  │  │  PostgreSQL       │
                                   │  (LLM Brain)     │   │  vector_kit.py     │  │  Auth + DB        │
                                   │  Free API Tier   │   │  builder.py        │  │  Free Tier        │
                                   └──────────────────┘   └────────────────────┘  └───────────────────┘
                                          │                         │
                                          │   DeckSpec JSON         │   Native .pptx
                                          └────────────────────────►│
                                                                     ▼
                                                           /tmp/nativeslide_outputs/
                                                           {uuid}.pptx
```

**Data flow:**
1. User uploads PDF or enters topic → FastAPI backend
2. PDF text extracted (pdfplumber) → summarized via Gemini Flash
3. Gemini returns structured `DeckSpec` JSON (slide layouts, content, speaker notes)
4. `DeckBuilder` renders each slide deterministically using `vector_kit.py` DrawingML primitives
5. Native `.pptx` file served back to user for download

---

## Tech Stack

| Layer | Technology | Hosting |
|---|---|---|
| **Frontend** | Next.js 14, Tailwind CSS, TypeScript | Cloudflare Pages (Free) |
| **Backend** | FastAPI, Python 3.11, Uvicorn | Oracle Cloud Always Free (ARM) |
| **AI Brain** | Google Gemini 1.5 Flash | Google AI Studio (Free Tier) |
| **Database** | Supabase PostgreSQL + Row Level Security | Supabase (Free Tier) |
| **Auth** | Supabase Auth (JWT) | Supabase (Free Tier) |
| **PPTX Engine** | python-pptx + native DrawingML `vector_kit` | Oracle Cloud |
| **Reverse Proxy** | Nginx + Certbot (Let's Encrypt) | Oracle Cloud |

**Total infrastructure cost: $0.00/month** for the first ~1,500 decks/day.

---

## Project Structure

```
nativeslide-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── core/         # Config, security, dependencies  
│   │   ├── engine/       # DrawingML PPTX generation engine
│   │   ├── models/       # Pydantic data models & DB schemas
│   │   └── services/     # PDF extraction, LLM orchestration
│   └── tests/
├── frontend/
│   └── src/
│       ├── app/          # Next.js 14 App Router pages
│       ├── components/
│       │   ├── ui/       # Reusable atomic components
│       │   ├── landing/  # Hero, Features, Pricing sections
│       │   └── studio/   # Creation studio, upload, preview
│       ├── hooks/        # Custom React hooks
│       ├── lib/          # API client, Supabase client, utils
│       └── types/        # TypeScript type definitions
├── docs/                 # Architecture docs, API reference
├── scripts/              # Deploy scripts, DB migrations
└── LICENSE               # BUSL-1.1
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- A free [Google AI Studio](https://aistudio.google.com/) API key
- A free [Supabase](https://supabase.com/) project

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/drnitz/nativeslide-ai.git
cd nativeslide-ai/backend

# Install dependencies with uv (recommended) or pip
pip install uv
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and fill in your API keys

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` and interactive docs at `http://localhost:8000/api/docs`.

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your backend URL

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`.

---

## Environment Variables

### Backend (`backend/.env`)

```env
# Google Gemini (free tier — https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase (free tier — https://supabase.com/)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_role_key_here

# JWT Security (generate: openssl rand -hex 32)
JWT_SECRET=your_random_32_char_secret_here

# Optional overrides
DEBUG=false
ALLOWED_ORIGINS=["https://nativeslide.pages.dev","http://localhost:3000"]
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set `NEXT_PUBLIC_API_URL` to your Oracle Cloud backend URL or custom domain in the Cloudflare Pages environment settings.

---

## Supported Themes

NativeSlide AI automatically detects your topic and applies the optimal theme. You can also override manually.

| Theme | Background | Primary Accent | Secondary Accent | Best For |
|---|---|---|---|---|
| **Space & Astronomy** | Cosmos Navy `#060B18` | Electric Cyan `#00E5FF` | Violet `#8B5CF6` | Space research, cosmology, physics |
| **AI / ML & Tech** | Cyber Slate `#0F172A` | Emerald Neon `#10B981` | Indigo `#6366F1` | Machine learning, neural networks, software |
| **Law & Judiciary** | Cream `#FAFAF7` | Burgundy `#881337` | Gold `#D97706` | Legal briefs, contracts, compliance |
| **Architecture & Design** | Pure White `#FFFFFF` | Terracotta `#C2410C` | Steel `#64748B` | Architecture, urban planning, product design |
| **Finance & Business** | Cloud White `#F8FAFC` | Royal Blue `#1D4ED8` | Teal `#0D9488` | Financial reports, investor decks, strategy |
| **Medicine & Clinical** | Clinical White `#F8FAFC` | Medical Teal `#00A896` | Rose `#E11D48` | Clinical research, pharmacology, case studies |
| **Education & Academic** | Warm White `#FFFBF5` | Academic Blue `#2563EB` | Purple `#7C3AED` | Lectures, theses, course material |
| **Engineering & Technical** | Light `#F8FAFC` | Sky Blue `#0EA5E9` | Orange `#F97316` | Engineering specs, technical documentation |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/generate/from-topic` | Generate deck from text topic |
| `POST` | `/api/generate/from-pdf` | Generate deck from uploaded PDF |
| `GET` | `/api/generate/status/{job_id}` | Poll job status |
| `GET` | `/api/generate/download/{job_id}` | Download generated `.pptx` |

Full API docs available at `/api/docs` (Swagger UI) when the backend is running.

---

## Contributing

Contributions are welcome for non-commercial, open-source use under the terms of the BUSL-1.1 license.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and write tests
4. Open a pull request with a clear description

Please read [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) before contributing to the engine layer.

---

## License

NativeSlide AI is licensed under the **Business Source License 1.1 (BUSL-1.1)**.

**What this means:**

- ✅ **Free for:** personal projects (<100 decks/month), academic research, non-commercial evaluation, open-source educational tooling
- ✅ **Converts to Apache 2.0** on **2029-10-27** (4 years from first release)
- ❌ **Commercial production use requires a commercial license**

For commercial licensing inquiries (SaaS deployments, enterprise on-premise, white-label), contact: **nativeslide@drnitz.dev**

See the full [LICENSE](./LICENSE) file for details.
