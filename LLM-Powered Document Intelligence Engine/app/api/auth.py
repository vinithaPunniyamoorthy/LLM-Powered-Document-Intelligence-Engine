from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.auth.password_hash import hash_password, verify_password
from app.database.db import get_db
from app.database.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user: dict, db: Session = Depends(get_db)):
    email = user.get("email")
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        name=user.get("name", "User"),
        email=email,
        password=hash_password(user["password"]),
        role=user.get("role", "user"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "user_id": db_user.id}


@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.get("email")).first()
    if not user or not verify_password(payload.get("password", ""), user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer", "role": user.role}
