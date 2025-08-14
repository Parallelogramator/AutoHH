from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.hh_client import HHClient
from app.config import get_settings, Settings
# Модели для получения текущего пользователя (будет реализовано в auth)
from app.models.user import User
from app.schemas.token import TokenData

# Заглушка для получения текущего пользователя
# В реальном проекте здесь будет проверка JWT токена
async def get_current_user(db: Session = Depends(lambda: next(get_db()))) -> User:
    user = db.query(User).filter(User.id == 1).first() # Заглушка: всегда возвращаем юзера с ID=1
    if user is None:
        user = User(id=1, email="test@example.com", name="Test User", hh_token=get_settings().HH_API_TOKEN)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_hh_client(settings: Settings = Depends(get_settings)) -> HHClient:
    # В реальном приложении токен должен браться из профиля пользователя
    return HHClient(token=settings.HH_API_TOKEN)

