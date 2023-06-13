from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.database import get_db
from app.models import Feed, User
from typing import Optional

router = APIRouter()


@router.get("")
async def get_feeds(
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    feeds: Optional[list[Feed]] = db.query(Feed).offset(skip).limit(limit).all()

    # Determine if the user is following each feed
    feed_ids_followed = set(feed.id for feed in user.feeds)
    for feed in feeds:
        feed.followed = feed.id in feed_ids_followed

    return feed


@router.post("/{feed_id}/follow")
def follow_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    feed = db.query(Feed).get(feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed in user.feeds:
        raise HTTPException(
            status_code=400, detail="You are already following this feed"
        )

    user.feeds.append(feed)
    db.commit()
    return {"message": "Successfully followed the feed"}


@router.delete("/{feed_id}/follow")
async def unfollow_feed(
    feed_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict[str, str]:
    feed: Optional[Feed] = db.query(Feed).get(feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")

    if feed not in user.feeds:
        raise HTTPException(
            status_code=400, detail="You are already not following this feed"
        )

    user.feeds.remove(feed)
    db.commit()
    return {"message": "Successfully unfollowed the feed"}
