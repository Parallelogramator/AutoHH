# AutoHH: Сервис автопоиска работы на hh.ru

Это стартовый каркас проекта по автоматизации поиска вакансий и откликов на hh.ru.
Проект реализован на FastAPI + LangChain + SQLAlchemy + Docker.

## Цель

Автоматизировать подбор вакансий и отклики на hh.ru: пользователь вводит навыки и опыт → сервис находит релевантные вакансии по API HH → при совпадении требований генерирует/подбирает резюме, пишет сопроводительное письмо (LLM+RAG) и отправляет отклик через HH API.

## Быстрый старт (локальный запуск)

1.  **Настройте окружение:**
    *   Скопируйте `.env.example` в `.env` и заполните своими данными (`OPENAI_API_KEY`, `HH_API_TOKEN` и др.).
    *   Убедитесь, что у вас установлен Docker и Docker Compose.

2.  **Сборка и запуск контейнеров:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Инициализация базы данных (Alembic):**
    *   Сначала нужно инициализировать Alembic внутри контейнера (только один раз).
        ```bash
        docker-compose exec api alembic init migrations
        ```
    * Затем откройте файл `autohh/app/db/migrations/env.py`, найдите строку `target_metadata = None` и замените её на:
      ```python
      from backend.app.models.base import Base
      target_metadata = Base.metadata
      ```
    *   Создайте первую миграцию:
        ```bash
        docker-compose exec api alembic revision --autogenerate -m "Initial migration"
        ```
    *   Примените миграцию:
        ```bash
        docker-compose exec api alembic upgrade head
        ```

4.  **Проверка работы:**
    *   API будет доступен по адресу `http://localhost:8000`.
    *   Интерактивная документация (Swagger UI) находится по адресу `http://localhost:8000/docs`.

5.  **Начало работы с API:**
    *   Используйте эндпоинты в Swagger для создания профиля, загрузки документов и запуска поиска.
    *   Воркер будет автоматически запускаться в отдельном контейнере и искать вакансии каждые 30 минут.
