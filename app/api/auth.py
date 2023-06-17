import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (LoginRequest, RegisterRequest, RegisterResponse,
                         TokenResponse)
from app.services import auth_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    logger.info("Login request received")
    token = auth_service.login(db, request.email, request.password)
    logger.info("Login successful")
    return TokenResponse(access_token=token)


@router.post("/register", response_model=RegisterResponse)
def register(
    request: RegisterRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    logger.info("Registration request received")
    user_id, message = auth_service.register(db, request.email, request.password)
    logger.info("Registration successful")
    return RegisterResponse(message=message, user_id=user_id)
