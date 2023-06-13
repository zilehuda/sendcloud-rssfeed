from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.feeds import router as feed_router
from app.api.posts import router as post_router
from app.auth.jwt_bearer import JWTBearer
from app.auth.service import get_current_user
from app.database import Base, engine, get_db
from app.services.rss_feed_service import RSSFeedService

# Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.get("/")
async def root(db: Session = Depends(get_db)):
    feed_url = "https://feeds.feedburner.com/tweakers/mixed"
    rss_feed_service: RSSFeedService = RSSFeedService(feed_url, db)
    rss_feed_service.fetch_and_save_feed()
    return {"msg": "created"}


@app.get(
    "/hello/{name}",
    dependencies=[Depends(JWTBearer())],
)
async def say_hello(name: str, user: dict = Depends(get_current_user)):
    return user
    return {"message": f"Hello {name}"}
