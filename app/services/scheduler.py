from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.session import SessionLocal
from app.services.search_and_match import periodic_search_and_match

scheduler = AsyncIOScheduler()

async def job_wrapper():
    """Обертка для создания сессии БД для фоновой задачи."""
    db = SessionLocal()
    try:
        print("Scheduler job started: periodic_search_and_match")
        await periodic_search_and_match(db)
        print("Scheduler job finished.")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Запускаем один раз при старте, потом по интервалу
        scheduler.add_job(job_wrapper, "interval", minutes=30, id="search_match_job", replace_existing=True)
        scheduler.start()
        print("Scheduler started.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler stopped.")
