from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    skills = Column(JSON, default=list)
    experience_json = Column(JSON)
    portfolio_links = Column(JSON, default=list)
    resume_variants = Column(JSON)
    keywords = Column(JSON, default=list)
    city = Column(String, nullable=True)
    salary_expectation = Column(Integer, nullable=True)
    auto_apply = Column(Boolean, default=False, nullable=False)
    require_review = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="profile")