from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.feeds import router as feed_router
from app.api.posts import router as post_router
from app.auth.jwt_bearer import JWTBearer
from app.auth.service import get_current_user
from app.database import Base, engine, get_db
from app.models import Feed
from app.services.rss_feed import RSSFeedCreator, RssFeedFetcher, RSSFeedUpdater

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
    feed_fetcher = RssFeedFetcher(feed_url)
    feed = db.query(Feed).filter_by(id=1).first()
    # rss_feed_service = RSSFeedCreator(feed_url, feed_fetcher, db)
    # rss_feed_service.fetch_and_save_feed()

    rss_feed_service = RSSFeedUpdater(feed.id, feed_fetcher, db)
    rss_feed_service.fetch_and_update_feed()
    return {"msg": "done"}


@app.get(
    "/hello/{name}",
)
async def say_hello(name: str):
    from .tasks import create_task

    task = create_task.delay(5, 5, 5)
    print(task)
    return {"message": "triggered"}
