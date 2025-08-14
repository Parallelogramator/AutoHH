from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models import User, Profile
from app.schemas.profile import ProfileIn, ProfileOut
from typing import List

router = APIRouter()

@router.post("/", response_model=ProfileOut, summary="Создать или обновить профиль пользователя")
def create_or_update_profile(profile_in: ProfileIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if profile:
        profile.skills = profile_in.skills
        profile.experience_json = [exp.model_dump() for exp in profile_in.experience]
        profile.keywords = profile_in.keywords
        profile.city = profile_in.city
        profile.salary_expectation = profile_in.salary_expectation
        profile.auto_apply = profile_in.auto_apply
        profile.require_review = profile_in.require_review
    else:
        profile = Profile(
            user_id=current_user.id,
            skills=profile_in.skills,
            experience_json=[exp.model_dump() for exp in profile_in.experience],
            keywords=profile_in.keywords,
            # --- ДОБАВЛЯЕМ НОВЫЕ ПОЛЯ ПРИ СОЗДАНИИ ---
            city=profile_in.city,
            salary_expectation=profile_in.salary_expectation,
            auto_apply=profile_in.auto_apply,
            require_review=profile_in.require_review
        )
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model=ProfileOut, summary="Получить профиль пользователя")
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
