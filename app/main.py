from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.config import get_settings
from app.routes import auth, profiles, vacancies, matches, docs
from app.services.scheduler import scheduler, start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application lifespan started.")
    yield
    print("Application lifespan finished.")

def create_app() -> FastAPI:
    app = FastAPI(
        title="AutoHH",
        version="1.0",
        description="Сервис автопоиска работы и откликов на hh.ru",
        lifespan=lifespan
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

async def main_worker_async():
    """Асинхронная основная функция, которая будет жить вечно."""
    print("Starting scheduler in Worker mode (async)...")
    start_scheduler()

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("Worker shutting down...")
        stop_scheduler()


def run_worker():
    """Эта функция - синхронная точка входа, вызываемая Docker'ом."""
    settings = get_settings()
    if settings.RUN_MODE == "worker":
        try:
            asyncio.run(main_worker_async())
        except KeyboardInterrupt:
            print("Worker process interrupted.")
