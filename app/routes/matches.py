from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db, get_current_user
from app.models import User, Match, Profile, Application
from app.schemas.match import MatchOut, GeneratedContent
from app.services import llm_chains, rag
from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

@router.get("/", response_model=List[MatchOut], summary="Получить список совпадений (матчей)")
def get_matches(status: str = "new", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    matches = db.query(Match).filter(Match.user_id == current_user.id, Match.status == status).all()
    return matches

@router.post("/{match_id}/generate", response_model=GeneratedContent, summary="Сгенерировать сопроводительное письмо")
def generate_content(match_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    match = db.query(Match).filter(Match.id == match_id, Match.user_id == current_user.id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    vector_store = rag.load_index(user_id=current_user.id)
    if not vector_store:
        raise HTTPException(status_code=400, detail="No RAG index found for user. Please upload documents.")

    retriever = vector_store.as_retriever()
    settings = get_settings()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-latest",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3,
        convert_system_message_to_human=True
    )

    chain = llm_chains.get_cover_letter_chain(llm, retriever)

    profile_text = f"Навыки: {', '.join(profile.skills)}. Опыт: {profile.experience_json}"
    vacancy_text = f"Название: {match.vacancy.title}. Описание: {match.vacancy.description}. Навыки: {', '.join(match.vacancy.skills)}"

    cover_letter = chain.invoke({
        "vacancy": vacancy_text,
        "profile": profile_text
    })

    return GeneratedContent(cover_letter=cover_letter, resume_summary="Summary generation not implemented yet.")