# auth/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (create_access_token, get_password_hash,
                                  verify_password)
from app.database import get_db
from app.models import User
from app.schemas import (LoginRequest, RegisterRequest, RegisterResponse,
                         TokenResponse)

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"id": user.id, "email": user.email})
    return TokenResponse(access_token=access_token)


@router.post("/register", response_model=RegisterResponse)
def register(
    request: RegisterRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(request.password)

    # Create the user
    user = User(
        email=request.email,
        password=hashed_password,
    )

    # Save the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    user_id = user.id
    message = "User registered successfully"

    return RegisterResponse(message=message, user_id=user_id)
