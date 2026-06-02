from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest

app = FastAPI(
    title="DocAgent Bench API",
    description="API for document ingestion and processing in the DocAgent Bench system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)

@app.get("/", summary="Root health check endpoint")
async def root():
    return {"message": "Welcome to the DocAgent Bench API. Use /docs for API documentation."}

@app.get("/health", summary="Check overall API health")
async def health():
    return {"api": "healthy", "version": "1.0.0"}