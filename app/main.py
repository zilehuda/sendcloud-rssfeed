from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.feeds import router as feed_router
from app.api.posts import router as post_router
from app.auth.jwt_bearer import JWTBearer, jwt_bearer
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
    dependencies=[Depends(jwt_bearer)],
)
app.include_router(
    feed_router,
    prefix="/api/feeds",
    tags=["feeds"],
    dependencies=[Depends(jwt_bearer)],
)
app.include_router(
    post_router,
    prefix="/api/posts",
    tags=["posts"],
    dependencies=[
        Depends(jwt_bearer),
    ],
)


@app.get("/")
async def root(db: Session = Depends(get_db)):
    feed_url = "https://feeds.feedburner.com/tweakers/mixed"
    # feed_url = "https://google.com/"
    feed_fetcher = RSSFeedFetcher(feed_url)
    feedi = feed_fetcher.fetch_feed()
    # if len(feedi.entries) == 0:
    return "OK"
    return feedi
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
