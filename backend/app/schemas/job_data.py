from pydantic import BaseModel, Field
from typing import List, Optional


class ParsedJobDescription(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)
    min_experience_years: Optional[int] = None