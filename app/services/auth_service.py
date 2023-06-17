import logging
from typing import Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (create_access_token, get_password_hash,
                                  verify_password)
from app.models import User
from app.services.user_service import UserRepository

logger = logging.getLogger(__name__)


def login(db: Session, email: str, password: str) -> str:
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        logging.warning(f"Invalid email or password for email: {email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"id": user.id, "email": user.email})
    return access_token


def register(db: Session, email: str, password: str) -> Tuple[int, str]:
    user_repository = UserRepository(db)
    existing_user = user_repository.get_user_by_email(email)
    if existing_user:
        logging.warning(f"Email already registered: {email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(password)

    user = User(email=email, password=hashed_password)

    user_repository.create_user(user)

    user_id = user.id
    message = "User registered successfully"
    return user_id, message
