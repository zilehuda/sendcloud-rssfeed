rssfeed-service/

````
├── app/
│ ├── api/
│ │ ├── __init__.py
│ │ ├── feeds.py
│ │ ├── posts.py
│ │ └── users.py
│ ├── background/
│ │ ├── __init__.py
│ │ └── feed_refresh.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── feed.py
│ │ ├── post.py
│ │ └── user.py
│ └── main.py
├── tests/
│ ├── __init__.py
│ ├── test_feeds.py
│ ├── test_posts.py
│ └── test_users.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```


- Fetch All Feeds:
Endpoint: GET /api/feeds
Description: Get a list of all available feeds.
Request body: None
Response: 200 OK with a list of feeds.

- List All Feed Posts:
Endpoint: GET /api/posts
Description: Get a list of all feed posts.
Request parameters:
read: true|false
feedId:
Response: 200 OK with a list of posts ordered by the date of the last update.

- Follow/un-follow feed
Endpoint: /feeds/{feed_id}/follow
Description: Follow or unfollow a specific feed.
Request body: None
Methods:
POST: Follow the feed. Response: 200 OK
DELETE: Unfollow the feed. Response: 200 OK

- Mark/unmark post as read
PUT: api/posts{post_id}/read 
Request body:
read: Boolean indicating the read status (true for read, false for unread).
