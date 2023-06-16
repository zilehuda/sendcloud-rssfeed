from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.models import User
from app.services import auth_service
from app.database import get_db
from app.schemas import LoginRequest, RegisterRequest, RegisterResponse, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token = auth_service.login(db, request.email, request.password)
    return TokenResponse(access_token=token)


@router.post("/register", response_model=RegisterResponse)
def register(
    request: RegisterRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    user_id, message = auth_service.register(db, request.email, request.password)
    return RegisterResponse(message=message, user_id=user_id)


@router.get("/hello")
def hello(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    print("d: ", user.email)
    return "hello"
