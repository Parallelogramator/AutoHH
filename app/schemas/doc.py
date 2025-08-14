from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DocOut(BaseModel):
    id: int
    kind: str
    title: str
    embedded_at: Optional[datetime] = None

    class Config:
        from_attributes = True
