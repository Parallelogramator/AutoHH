import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, ARRAY, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from .enums import MatchStatusEnum


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True) # <-- Добавлен index
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False, index=True) # <-- Добавлен index
    score = Column(Float, nullable=False)
    gaps = Column(ARRAY(String))
    status = Column(Enum(MatchStatusEnum), default=MatchStatusEnum.NEW, nullable=False) # <-- ИСПОЛЬЗУЕМ ENUM
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="matches")
    vacancy = relationship("Vacancy", back_populates="matches")
    application = relationship("Application", back_populates="match", uselist=False, cascade="all, delete-orphan")
