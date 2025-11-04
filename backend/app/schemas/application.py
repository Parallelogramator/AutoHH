from pydantic import BaseModel
from typing import Optional, Dict, Any
import datetime

class ApplicationOut(BaseModel):
    id: int
    match_id: int
    resume_id: str
    cover_letter: str
    sent_at: datetime.datetime
    hh_response_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
