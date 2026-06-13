import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.middleware import get_current_user
from app.database.db import get_db
from app.database.models import Document
from app.services.chunking import split_text
from app.services.embedding_service import generate_embeddings
from app.services.pdf_parser import extract_text_from_file

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="Missing filename")

    upload_dir = Path("documents")
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / file.filename
    content = file.file.read()
    file_path.write_bytes(content)

    try:
        text = extract_text_from_file(str(file_path))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    chunks = split_text(text)
    embeddings = generate_embeddings(chunks)
    _ = embeddings

    db_doc = Document(filename=file.filename, content=text[:5000], uploaded_by=current_user.id)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return {"message": "Document uploaded", "document_id": db_doc.id, "chunks": len(chunks)}


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return [{"id": doc.id, "filename": doc.filename, "uploaded_by": doc.uploaded_by} for doc in docs]
