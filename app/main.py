import logging
import sys

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.feeds import router as feed_router
from app.api.posts import router as post_router
from app.auth.jwt_bearer import JWTBearer
from app.database import get_db
from app.models import Feed
from app.services.rss_feed_services import RSSFeedCreator

log_format = "%(asctime)s [%(levelname)s] logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s"  # noqa
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    feed_router,
    prefix="/api/feeds",
    tags=["feeds"],
    dependencies=[Depends(JWTBearer())],
)
app.include_router(
    post_router,
    prefix="/api/posts",
    tags=["posts"],
    dependencies=[
        Depends(JWTBearer()),
    ],
)
