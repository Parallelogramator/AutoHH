from sqlalchemy import Column, Integer, String, JSON, ARRAY, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True) # Добавлен unique=True для one-to-one
    skills = Column(ARRAY(String), default=[])
    experience_json = Column(JSON)
    portfolio_links = Column(ARRAY(String), default=[])
    resume_variants = Column(JSON)
    keywords = Column(ARRAY(String), default=[])

    city = Column(String, nullable=True)
    salary_expectation = Column(Integer, nullable=True)
    auto_apply = Column(Boolean, default=False, nullable=False, server_default='false')
    require_review = Column(Boolean, default=True, nullable=False, server_default='true')

    user = relationship("User", back_populates="profile")
