import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    resume_id = Column(String)
    cover_letter = Column(Text)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    hh_response_json = Column(JSON)

    match = relationship("Match", back_populates="application")