from sqlalchemy.orm import Session
from app.models import User, Profile, Vacancy, Match
from app.services.hh_client import HHClient
from app.services.matcher import compute_score
import json

async def periodic_search_and_match(db: Session):
    """
    Основная логика, выполняемая по расписанию.
    1. Получает всех пользователей и их профили.
    2. Для каждого пользователя выполняет поиск вакансий по ключевым словам.
    3. Сохраняет новые вакансии в БД.
    4. Для каждой новой вакансии считает скор совпадения.
    5. Если скор выше порога, создает запись Match.
    """
    print("Executing periodic search and match...")
    users = db.query(User).all()
    for user in users:
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        if not profile:
            print(f"User {user.id} has no profile, skipping.")
            continue

        print(f"Processing user {user.id} with keywords: {profile.keywords}")
        hh_client = HHClient(token=user.hh_token)
        search_query = " OR ".join(profile.keywords) if profile.keywords else "Python"

        try:
            vacancies_data = await hh_client.search_vacancies(text=search_query)
        except Exception as e:
            print(f"Error fetching vacancies for user {user.id}: {e}")
            continue

        for item in vacancies_data.get("items", []):
            exists = db.query(Vacancy).filter(Vacancy.hh_id == item["id"]).first()
            if exists:
                continue

            skills = [s['name'] for s in item.get('key_skills', [])]
            new_vacancy = Vacancy(
                hh_id=item["id"],
                title=item.get("name"),
                company=item.get("employer", {}).get("name"),
                url=item.get("alternate_url"),
                skills=json.dumps(skills),
                description=item.get('snippet', {}).get('requirement', '')
            )
            db.add(new_vacancy)
            db.flush()

            score_data = compute_score(profile.skills, skills)
            print(f"Vacancy {new_vacancy.title} score: {score_data['score']}")

            if score_data["score"] > 0.3:
                new_match = Match(
                    user_id=user.id,
                    vacancy_id=new_vacancy.id,
                    score=score_data["score"],
                    gaps=json.dumps(score_data["gaps"]),
                    status="new"
                )
                db.add(new_match)

        db.commit()
    print("Periodic search and match finished.")