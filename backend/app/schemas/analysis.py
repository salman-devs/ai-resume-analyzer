from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnalysisResponse(BaseModel):
    id: int
    ats_score: int
    matched_keywords: List[str]
    missing_keywords: List[str]
    ai_feedback: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AnalysisListItem(BaseModel):
    id: int
    ats_score: int
    created_at: datetime

    class Config:
        from_attributes = True