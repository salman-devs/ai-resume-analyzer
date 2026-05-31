from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime


class AnalysisResponse(BaseModel):
    id: int
    filename: Optional[str] = None
    ats_score: int
    matched_keywords: List[str]
    missing_keywords: List[str]
    ai_feedback: Optional[Any] = None
    job_description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisListItem(BaseModel):
    id: int
    filename: Optional[str] = None
    ats_score: int
    job_description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    total: int
    avg_score: int
    best_score: int
    latest_score: Optional[int] = None