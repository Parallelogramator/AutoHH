from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import Runnable
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.retriever import BaseRetriever

COVER_LETTER_PROMPT_TEMPLATE = """
Ты — карьерный консультант и tech writer.
Твоя задача: написать краткое (5-8 предложений) и убедительное сопроводительное письмо на русском языке, основываясь на данных о вакансии, профиле кандидата и релевантных кейсах из его опыта.

Правила:
1.  **Стиль**: Деловой, вежливый, энергичный, без воды.
2.  **Структура**: Начни с приветствия. Подчеркни 2-3 ключевых совпадения между требованиями вакансии и опытом кандидата. Если есть пробелы в навыках, мягко укажи, чем их можно компенсировать (например, "хотя у меня нет прямого опыта с X, мой опыт с Y позволил мне развить схожие навыки..."). Заверши призывом к действию.
3.  **Опора на факты**: Не выдумывай информацию. Используй только то, что дано в профиле и контексте.
4.  **Краткость**: Не более 8 предложений.

---
ВАКАНСИЯ:
{vacancy}

---
ПРОФИЛЬ КАНДИДАТА:
{profile}

---
КОНТЕКСТ ИЗ ПРОЕКТОВ И РЕЗЮМЕ КАНДИДАТА (используй это для подтверждения навыков):
{context}
---

Сгенерируй только текст сопроводительного письма.
"""

def get_cover_letter_chain(llm: ChatGoogleGenerativeAI, retriever: BaseRetriever) -> Runnable:
    prompt = ChatPromptTemplate.from_template(COVER_LETTER_PROMPT_TEMPLATE)

    def retrieve_context(inputs: dict) -> str:
        query = f"Требования вакансии: {inputs['vacancy']}"
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join([d.page_content for d in docs])

    chain = (
        {
            "context": retrieve_context,
            "vacancy": lambda x: x["vacancy"],
            "profile": lambda x: x["profile"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain