# Agentic AI Remote Sensing Platform — Backend

This repository contains the backend foundation for the Agentic AI Remote Sensing Automation Platform.

Quick start

1. Copy `.env.example` to `.env` and fill in `MONGODB_URI` (do NOT commit secrets).

2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Run the app locally:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Health endpoint: `GET /api/v1/health`

Project layout: see folder structure under `backend/`.
