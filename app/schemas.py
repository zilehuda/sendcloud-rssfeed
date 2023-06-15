from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


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


class Feed(BaseModel):
    id: int
    title: str
    feed_url: str
    website: str
    logo: str
    followed: bool
    created_at: datetime

    class Config:
        orm_mode = True


class GetFeedsResponse(BaseModel):
    feeds: list[Feed]


class ResponseWithMessage(BaseModel):
    message: str


class Post(BaseModel):
    title: str
    post_id: str
    author: str
    feed_id: int
    published_at: datetime
    id: int
    summary: str
    post_url: str
    created_at: datetime
    is_read: bool

    class Config:
        orm_mode = True


class GetPostsResponse(BaseModel):
    posts: list[Post]
