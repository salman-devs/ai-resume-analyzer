from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse, AnalysisListItem
from app.services.pdf_service import extract_text_from_pdf
from app.services.ats_service import calculate_ats_score
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

router = APIRouter(prefix="/analysis", tags=["Analysis"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=AnalysisResponse, status_code=201)
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # validate file size (max 5MB)
    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be under 5MB")

    # extract text from PDF
    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read PDF. Make sure it is not corrupted.")

    if not resume_text:
        raise HTTPException(status_code=400, detail="PDF appears to be empty or has no readable text.")

    # calculate ATS score
    result = calculate_ats_score(resume_text, job_description)

    # save to database
    analysis = Analysis(
        user_id=current_user.id,
        resume_text=resume_text,
        job_description=job_description,
        ats_score=result["ats_score"],
        matched_keywords=result["matched_keywords"],
        missing_keywords=result["missing_keywords"],
        ai_feedback=None
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

@router.get("/", response_model=List[AnalysisListItem])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Analysis).filter(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc()).all()

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis