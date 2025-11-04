import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base
from .enums import MatchStatusEnum

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    gaps = Column(JSON)
    status = Column(Enum(MatchStatusEnum), default=MatchStatusEnum.NEW)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="matches")
    vacancy = relationship("Vacancy", back_populates="matches")
    application = relationship("Application", back_populates="match", uselist=False, cascade="all, delete-orphan")