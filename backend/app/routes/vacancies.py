from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db
from app.models import Vacancy
from app.schemas.vacancy import VacancyOut
from app.services.search_and_match import periodic_search_and_match

router = APIRouter()

@router.get("/", response_model=List[VacancyOut], summary="Получить список всех найденных вакансий")
def get_vacancies(db: Session = Depends(get_db)):
    vacancies = db.query(Vacancy).order_by(Vacancy.indexed_at.desc()).limit(100).all()
    return vacancies

@router.post("/refresh", summary="Принудительно запустить поиск и матчинг вакансий (для отладки)")
async def refresh_vacancies(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        background_tasks.add_task(periodic_search_and_match, db)
        return {"status": "ok", "message": "Search and match process started in the background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))