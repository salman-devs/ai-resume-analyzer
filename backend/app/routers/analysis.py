from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse, AnalysisListItem, StatsResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.ats_service import calculate_ats_score
from app.tasks import run_ai_feedback

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/stats", response_model=StatsResponse)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )
    if not analyses:
        return StatsResponse(total=0, avg_score=0, best_score=0, latest_score=None)

    scores = [a.ats_score for a in analyses]
    return StatsResponse(
        total=len(analyses),
        avg_score=round(sum(scores) / len(scores)),
        best_score=max(scores),
        latest_score=scores[0],
    )


@router.post("/", response_model=AnalysisResponse, status_code=201)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 5MB")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="PDF appears to be empty or contains no readable text.",
        )

    result = calculate_ats_score(resume_text, job_description)

    task = run_ai_feedback.delay(
        resume_text,
        job_description,
        result["ats_score"],
        result["matched_keywords"],
        result["missing_keywords"],
    )
    ai_feedback = task.get(timeout=30)

    analysis = Analysis(
        user_id=current_user.id,
        filename=file.filename,
        resume_text=resume_text,
        job_description=job_description,
        ats_score=result["ats_score"],
        matched_keywords=result["matched_keywords"],
        missing_keywords=result["missing_keywords"],
        ai_feedback=ai_feedback,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/", response_model=List[AnalysisListItem])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.delete("/{analysis_id}", status_code=204)
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    db.delete(analysis)
    db.commit()