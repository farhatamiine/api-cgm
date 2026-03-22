from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from db.database import get_db
from db.models.user import User

auth_router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


@auth_router.post("/register", status_code=201)
def register(
    data: RegisterRequest, db: Session = Depends(get_db)
) -> dict[str, Any]:
    user = User(email=data.email, hashed_password=get_password_hash(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Email already registered")
    db.refresh(user)
    return {"id": user.id, "email": user.email}


@auth_router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            401, "Incorrect email or password", headers={"WWW-Authenticate": "Bearer"}
        )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
