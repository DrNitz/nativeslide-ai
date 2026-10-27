---
title: NativeSlide AI Backend
emoji: 📑
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: other
---

# NativeSlide AI — Backend Engine

High-performance FastAPI service generating 100% native DrawingML editable PowerPoint presentations.

### Endpoints
- `GET /health` — Service health check
- `POST /api/generate/from-topic` — Generate deck from prompt or text outline
- `POST /api/generate/from-pdf` — Extract PDF and generate deck
- `GET /api/generate/download/{job_id}` — Download generated `.pptx`
