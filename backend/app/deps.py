from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.hh_client import HHClient
from app.config import get_settings, Settings
from app.models.user import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Заглушка для получения текущего пользователя
# В реальном проекте здесь будет проверка JWT токена
async def get_current_user(db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> User:
    user = db.query(User).filter(User.id == 1).first()  # Заглушка: всегда возвращаем юзера с ID=1
    if user is None:
        user = User(
            id=1,
            email="test@example.com",
            name="Test User",
            hh_token=settings.HH_API_TOKEN
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_hh_client(current_user: User = Depends(get_current_user)) -> HHClient:
    return HHClient(token=current_user.hh_token)