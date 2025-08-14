from pydantic import BaseModel, Field
from typing import List, Optional
from .vacancy import VacancyOut
from app.models.enums import MatchStatusEnum


class MatchOut(BaseModel):
    id: int
    score: float
    gaps: List[str]
    status: MatchStatusEnum
    vacancy: VacancyOut

    class Config:
        from_attributes = True

class GeneratedContent(BaseModel):
    cover_letter: str
    resume_summary: str
