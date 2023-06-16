from fastapi import HTTPException

from app.auth.jwt_handler import create_access_token, verify_password, get_password_hash
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, RegisterResponse, TokenResponse
from app.services.user_service import UserRepository
from sqlalchemy.orm import Session


def login(db: Session, email: str, password: str) -> str:
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"id": user.id, "email": user.email})
    return access_token


def register(db: Session, email: str, password: str) -> (int, str):
    user_repository = UserRepository(db)
    existing_user = user_repository.get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(password)

    user = User(email=email, password=hashed_password)

    user_repository.create_user(user)

    user_id = user.id
    message = "User registered successfully"
    return user_id, message
