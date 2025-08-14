from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    user_id: Optional[int] = None

class HHConnect(BaseModel):
    hh_token: str

