from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.analysis import Analysis

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    total_users = db.query(func.count(User.id)).scalar()
    total_analyses = db.query(func.count(Analysis.id)).scalar()
    avg_score = db.query(func.avg(Analysis.ats_score)).scalar()
    top_score = db.query(func.max(Analysis.ats_score)).scalar()

    return {
        "total_users": total_users,
        "total_analyses": total_analyses,
        "avg_score": round(float(avg_score), 1) if avg_score else 0,
        "top_score": int(top_score) if top_score else 0,
    }


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "total_analyses": len(u.analyses),
        }
        for u in users
    ]


@router.get("/analyses")
def get_recent_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    analyses = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": a.id,
            "filename": a.filename,
            "ats_score": a.ats_score,
            "created_at": a.created_at.isoformat() if a.created_at else None,
            "user_id": a.user_id,
        }
        for a in analyses
    ]