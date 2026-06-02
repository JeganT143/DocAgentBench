# DocAgent Bench

A production-grade AI document evaluation benchmarking system.

## What It Does

DocAgent Bench benchmarks the full RAG (Retrieval-Augmented Generation) 
pipeline on real document corpora — PubMed abstracts and SEC 10-K filings.

**Pipeline:**
1. Document ingestion via REST API
2. Text extraction with PaddleOCR 3.5
3. Chunk reranking with Ettin Reranker
4. Answer generation with Gemini 2.5 Flash
5. Quality evaluation with RAGAS (faithfulness + context precision)
6. Public leaderboard on GitHub Pages

## Tech Stack

- Python 3.12
- FastAPI 0.115+ with Pydantic v2
- Docker + Docker Compose
- PaddleOCR 3.5 (Transformers backend)
- Ettin Reranker (HuggingFace Transformers v5)
- Google Gemini 2.5 Flash (Managed Agent)
- RAGAS (faithfulness, context_precision)
- Streamlit (leaderboard UI)
- GitHub Actions (CI/CD)

## Quick Start

### Prerequisites
- Docker 24+
- Docker Compose v2

### Run Locally

1. Clone the repository:
   
   git clone https://github.com/YOUR_USERNAME/DocAgentBench.git
   cd DocAgentBench

2. Create your environment file:
   
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY

3. Start all services:
   
   docker compose up --build

4. Access the API docs:
   
   http://localhost:8000/docs

5. Access the leaderboard:
   
   http://localhost:8501

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /ingest/ | Upload a document for benchmarking |
| GET | /ingest/health | Check ingestion service health |
| GET | /health | Full system health check |

## Project Structure

    docagent-bench/
    ├── api/                    # FastAPI service
    │   ├── main.py             # Application entry point
    │   ├── routers/            # Endpoint definitions
    │   ├── models/             # Pydantic schemas
    │   └── Dockerfile
    ├── streamlit_app/          # Leaderboard UI
    ├── data/uploads/           # Document storage (gitignored)
    ├── docker-compose.yml
    └── .env.example            # Environment variable template

## Build Status

Day 1 complete: Docker + FastAPI + document ingestion endpoint
Day 2 in progress: PaddleOCR + Ettin Reranker + Gemini Agent

## License

MIT