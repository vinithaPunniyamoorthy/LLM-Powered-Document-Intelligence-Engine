from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.middleware import get_current_user
from app.database.db import get_db
from app.database.models import Document, QueryLog, User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        return {"error": "Admin access required"}

    return {
        "total_users": db.query(User).count(),
        "total_documents": db.query(Document).count(),
        "total_queries": db.query(QueryLog).count(),
    }
