import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    level = Column(String, default="INFO")
    message = Column(String)
    meta_json = Column(JSON)  # Можно оставить
    ts = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="logs")