import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, analysis
from app.routers import jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s  %(message)s",
)

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0",
    description="Upload a PDF resume and get an ATS score + AI-powered feedback.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(jobs.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "AI Resume Analyzer API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}