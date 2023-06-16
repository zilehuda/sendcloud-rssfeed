from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.feeds import router as feed_router
from app.api.posts import router as post_router
from app.auth.jwt_bearer import JWTBearer
from app.database import get_db
from app.models import Feed
from app.services.rss_feed_services import (
    RSSFeedFetcher,
    RSSFeedUpdater,
    RSSFeedCreator,
)

# Base.metadata.create_all(bind=engine)

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


@app.get("/")
async def root(db: Session = Depends(get_db)):
    feed_url = "https://feeds.feedburner.com/tweakers/mixed"
    feed_fetcher = RSSFeedFetcher(feed_url)

    # feeds = db.query(Feed).all()
    feed = db.query(Feed).filter_by(id=1).first()

    rss_feed_service = RSSFeedCreator(db, feed_url)
    rss_feed_service.fetch_and_save_feed()
    # feeds = db.query(Feed).all()
    # rss_feed_service = RSSFeedUpdater(db, feed.id)
    # rss_feed_service.fetch_and_update_feed()
    return {"msg": "done"}


@app.get(
    "/hello/{name}",
)
async def say_hello(name: str):
    from app.tasks import refresh_feeds

    task = refresh_feeds()
    print(task)
    return {"message": "triggered"}
