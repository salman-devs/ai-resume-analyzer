from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.jobs_service import fetch_and_score_jobs

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/search")
async def search_jobs(
    title: str = Query(..., description="Job title to search for"),
    location: str = Query("india", description="Location to search in"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.latest_resume_text:
        raise HTTPException(
            status_code=400,
            detail="No resume found. Please run an analysis first before searching jobs.",
        )

    jobs = await fetch_and_score_jobs(
        resume_text=current_user.latest_resume_text,
        title=title,
        location=location,
    )

    if not jobs:
        raise HTTPException(
            status_code=404,
            detail="No jobs found for your search. Try different keywords.",
        )

    return {"jobs": jobs, "total": len(jobs)}