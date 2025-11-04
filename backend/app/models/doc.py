from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from .enums import DocKindEnum

class Doc(Base):
    __tablename__ = "docs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    kind = Column(Enum(DocKindEnum))
    title = Column(String)
    text = Column(Text)
    meta_json = Column(JSON)
    embedded_at = Column(DateTime)

    user = relationship("User", back_populates="docs")