from typing import Optional, Union

from fastapi import Depends
from jose import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User

from .constants import JWT_ALGORITHM
from .jwt_bearer import JWTBearer


async def get_current_user(
    token: str = Depends(JWTBearer()), db: Session = Depends(get_db)
) -> Optional[User]:
    # skipping verify since its already verified in JWTBearer
    payload: dict[str, Union[int, str]] = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )
    user_id = payload.get("id")
    user = db.get(User, user_id)
    return user
