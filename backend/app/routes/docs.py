from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models import User, Doc
from app.services import rag
import datetime

router = APIRouter()

@router.post("/upload", summary="Загрузить документ для RAG")
def upload_doc(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if file.content_type not in ["text/plain", "text/markdown"]:
        raise HTTPException(status_code=400, detail="Only .txt and .md files are supported for now")

    content = file.file.read().decode("utf-8")

    # Индексируем
    rag.build_or_update_index(user_id=current_user.id, texts=[content])

    # Сохраняем в БД
    doc = Doc(
        user_id=current_user.id,
        kind="resume", # Определять по содержимому
        title=file.filename,
        text=content,
        embedded_at=datetime.datetime.utcnow()
    )
    db.add(doc)
    db.commit()

    return {"filename": file.filename, "message": "File processed and indexed"}
