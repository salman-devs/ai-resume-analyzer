from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

import logging
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse, AnalysisListItem, StatsResponse
from app.services.pdf_service import validate_and_extract_resume, ResumeValidationError
from app.services.ats_service import calculate_ats_score
from app.tasks import run_ai_feedback
from app.services.resume_parser_service import parse_resume

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
    file_bytes = await file.read()
    job_description = job_description.strip() if job_description else ""

    try:
        resume_text = validate_and_extract_resume(file.filename, file_bytes)
    except ResumeValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    try:
        parsed_resume = parse_resume(resume_text).model_dump()
    except Exception as exc:
        logging.getLogger(__name__).warning("Resume parsing failed, continuing without it: %s", exc)
        parsed_resume = None

    if job_description:
        result = calculate_ats_score(resume_text, job_description)
        task = run_ai_feedback.delay(
            resume_text,
            job_description,
            result["ats_score"],
            result["matched_keywords"],
            result["missing_keywords"],
        )
        ai_feedback = task.get(timeout=30)
        ats_score = result["ats_score"]
        matched_keywords = result["matched_keywords"]
        missing_keywords = result["missing_keywords"]
    else:
        ats_score = 0
        matched_keywords = []
        missing_keywords = []
        ai_feedback = {
            "overall_assessment": "Resume saved successfully. No job description provided.",
            "strengths": [],
            "improvements": [],
            "keyword_tips": "",
            "formatting_tips": "",
            "score_breakdown": {"keyword_match": 0, "estimated_readability": 0, "estimated_relevance": 0},
        }

    # save latest resume text to user profile
    current_user.latest_resume_text = resume_text
    db.add(current_user)

    analysis = Analysis(
        user_id=current_user.id,
        filename=file.filename,
        resume_text=resume_text,
        job_description=job_description,
        ats_score=ats_score,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        ai_feedback=ai_feedback,
        parsed_resume = parsed_resume,
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