from app.celery_app import app
from app.constants import FetchStatus
from app.database import get_db
from app.models import Feed


@app.task(name="refresh_feeds")
def refresh_feeds():
    db = next(get_db())
    feeds = db.query(Feed).filter_by(fetch_status=FetchStatus.COMPLETED.value).all()
    for feed in feeds:
        print("haha")
        # refresh_feed.delay(feed.id)
