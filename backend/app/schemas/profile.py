from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Dict, Any

class ExperienceItem(BaseModel):
    role: str
    company: str
    start: str
    end: Optional[str] = None
    responsibilities: List[str]

class ProfileIn(BaseModel):
    skills: List[str] = Field(..., example=["Python", "FastAPI", "Docker"])
    experience: List[ExperienceItem]
    city: Optional[str] = "Москва"
    salary_expectation: Optional[int] = 150000
    keywords: List[str] = Field(default=[], example=["backend", "data engineer"])
    auto_apply: bool = False
    require_review: bool = True

class ProfileOut(BaseModel):
    id: int
    skills: List[str]
    city: Optional[str]
    salary_expectation: Optional[int]
    keywords: List[str]
    auto_apply: bool
    require_review: bool

    experience_json: Optional[List[Any]] = Field(default=None, exclude=True)
    @computed_field
    @property
    def experience(self) -> List[ExperienceItem]:
        if self.experience_json:
            return [ExperienceItem.model_validate(item) for item in self.experience_json]
        return []

    class Config:
        from_attributes = True
