from pydantic import BaseModel
from typing import List, Optional

class VacancyOut(BaseModel):
    id: int
    hh_id: str
    title: str
    company: str
    city: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: Optional[str] = None
    skills: List[str]
    url: str
    match_score: Optional[float] = None

    class Config:
        from_attributes = True
