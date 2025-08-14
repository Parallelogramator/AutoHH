from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.token import HHConnect

router = APIRouter()

@router.post("/hh/connect", summary="Привязать или обновить токен HH для пользователя")
def connect_hh(data: HHConnect, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.hh_token = data.hh_token
    db.commit()
    return {"message": "HH token updated successfully."}
