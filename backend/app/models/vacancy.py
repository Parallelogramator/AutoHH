import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    hh_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String)
    city = Column(String)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(String)
    skills = Column(JSON)
    description = Column(Text)
    url = Column(String)
    raw_json = Column(JSON)
    indexed_at = Column(DateTime, default=datetime.datetime.utcnow)
    matches = relationship("Match", back_populates="vacancy")