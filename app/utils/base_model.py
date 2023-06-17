#  type: ignore

import datetime


from sqlalchemy import Column, DateTime, Integer

from app.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
