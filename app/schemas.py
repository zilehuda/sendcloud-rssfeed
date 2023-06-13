from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {"email": "zilehuda@rss.feed", "password": "sendcloud"}
        }


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "zilehuda@rss.feed", "password": "sendcloud"}
        }


class TokenResponse(BaseModel):
    access_token: str


class RegisterResponse(BaseModel):
    message: str
    user_id: int
