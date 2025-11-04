import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from app.config import get_settings


def get_user_index_path(user_id: int) -> str:
    # ... без изменений ...
    settings = get_settings()
    path = os.path.join(settings.EMBED_INDEX_PATH, f"user_{user_id}")
    os.makedirs(path, exist_ok=True)
    return path


def build_or_update_index(user_id: int, texts: List[str]) -> FAISS:
    settings = get_settings()
    index_path = get_user_index_path(user_id)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents(texts)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_API_KEY)

    if os.path.exists(os.path.join(index_path, "index.faiss")):
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(docs)
    else:
        vector_store = FAISS.from_documents(docs, embeddings)

    vector_store.save_local(index_path)
    return vector_store


def load_index(user_id: int) -> FAISS:
    settings = get_settings()
    index_path = get_user_index_path(user_id)
    if not os.path.exists(os.path.join(index_path, "index.faiss")):
        return None

    # ИЗМЕНЕНИЕ: Используем эмбеддинги от Google
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_API_KEY)
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)