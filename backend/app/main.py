from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import create_db_and_tables
from app.routes import auth, matches, profiles, vacancies, docs
from app.services.search_and_match import periodic_search_and_match
from app.db.session import SessionLocal

create_db_and_tables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application lifespan started.")
    # Запуск фоновой задачи при старте
    background_tasks = BackgroundTasks()
    db = SessionLocal()
    try:
        background_tasks.add_task(periodic_search_and_match, db)
    finally:
        db.close()
    yield
    print("Application lifespan finished.")

def create_app() -> FastAPI:
    app = FastAPI(
        title="AutoHH",
        version="1.0",
        description="Сервис автопоиска работы и откликов на hh.ru",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
    app.include_router(docs.router, prefix="/docs", tags=["Documents (RAG)"])
    app.include_router(vacancies.router, prefix="/vacancies", tags=["Vacancies"])
    app.include_router(matches.router, prefix="/matches", tags=["Matches & Applications"])

    @app.get("/", tags=["Health Check"])
    def read_root():
        return {"status": "ok"}

    return app

app = create_app()