import httpx
from typing import List, Dict, Any

class HHClient:
    BASE_URL = "https://api.hh.ru"

    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}",
                        "User-Agent": "AutoHH/1.0 (daniil200307@outlook.com)"}
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)

    async def search_vacancies(self, text: str, area: int = 1, per_page: int = 50, page: int = 0) -> Dict:
        """Поиск вакансий. area=1 это Москва."""
        params = {"text": text, "area": area, "per_page": per_page, "page": page}
        response = await self.client.get(f"{self.BASE_URL}/vacancies", params=params)
        response.raise_for_status()
        return response.json()

    async def get_vacancy(self, vacancy_id: str) -> Dict:
        response = await self.client.get(f"{self.BASE_URL}/vacancies/{vacancy_id}")
        response.raise_for_status()
        return response.json()

    async def get_my_resumes(self) -> Dict:
        response = await self.client.get(f"{self.BASE_URL}/resumes/mine")
        response.raise_for_status()
        return response.json()

    async def apply(self, vacancy_id: str, resume_id: str, letter: str) -> Dict:
        payload = {
            "resume_id": resume_id,
            "vacancy_id": vacancy_id,
            "message": letter
        }
        response = await self.client.post(f"{self.BASE_URL}/negotiations", json=payload)
        response.raise_for_status()
        return response.json()