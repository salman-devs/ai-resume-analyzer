from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.jobs_service import fetch_and_score_jobs, extract_job_title
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/search")
async def search_jobs(
    location: str = Query("india"),
    title: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.latest_resume_text:
        raise HTTPException(
            status_code=400,
            detail="No resume found. Please upload a resume to find matching jobs.",
        )

    job_title = title if title else extract_job_title(current_user.latest_resume_text)
    jobs = await fetch_and_score_jobs(
        resume_text=current_user.latest_resume_text,
        title=job_title,
        location=location,
    )

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found. Try a different location.")

    return {"jobs": jobs, "total": len(jobs), "searched_title": job_title}


@router.post("/search-with-resume")
async def search_jobs_with_resume(
    file: UploadFile = File(...),
    location: str = Form("india"),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 5MB")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="PDF appears empty or has no readable text.")

    # save as latest resume
    current_user.latest_resume_text = resume_text
    db.add(current_user)
    db.commit()

    job_title = title if title else extract_job_title(resume_text)
    jobs = await fetch_and_score_jobs(
        resume_text=resume_text,
        title=job_title,
        location=location,
    )

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found. Try a different location.")

    return {"jobs": jobs, "total": len(jobs), "searched_title": job_title}