from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import QueryLog
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import VectorStore

router = APIRouter(tags=["query"])

vector_store = VectorStore("./chroma_db")


@router.post("/query")
def query_documents(payload: dict, db: Session = Depends(get_db)):
    question = payload.get("question", "")
    if not question.strip():
        return {"answer": "Please provide a question to search the documents."}

    query_embedding = generate_embeddings([question])[0]
    results = vector_store.search(query_embedding, top_k=4)
    context = "\n\n".join(item["text"] for item in results)

    answer = (
        "Answer based on available document context."
        if not context.strip()
        else f"Based on the uploaded documents: {context[:1200]}"
    )

    db.add(QueryLog(user_id=None, question=question, response=answer))
    db.commit()

    return {"answer": answer, "sources": [item["id"] for item in results]}
