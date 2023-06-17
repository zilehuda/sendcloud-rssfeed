# RSS Feed Service
This repository contains the code for an RSS feed service. 
It provides functionalities such as: 
- Add new feed.
- Follow/un-follow feed.
- force refresh new posts from feeds.
- mark posts as read/unread.
- scheduler to refresh posts every 5 minutes.
- Back-off mechanism with 2, 5 and 8 minutes.

Tested the app on the following two feeds.
1. http://www.nu.nl/rss/Algemeen 
2. https://feeds.feedburner.com/tweakers/mixed

## Directory Structure
The repository has the following directory structure:
````
├── .env.example
├── Dockerfile
├── alembic
│   ├── ...
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── feeds.py
│   │   └── posts.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── jwt_bearer.py
│   │   ├── jwt_handler.py
│   │   └── service.py
│   ├── celery_app.py
│   ├── config.py
│   ├── constants.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── feed_repository.py
│   │   ├── post_repository.py
│   │   └── user_repository.py
│   ├── schemas.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── feed_manager_service.py
│   │   ├── feed_service.py
│   │   ├── post_service.py
│   │   ├── rss_feed_services
│   │   │   ├── __init__.py
│   │   │   ├── feed_creator.py
│   │   │   ├── feed_fetcher.py
│   │   │   └── feed_updater.py
│   │   └── user_service.py
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── fetch_and_assign_feed_to_user.py
│   │   ├── force_refresh_feed.py
│   │   ├── refresh_feed.py
│   │   └── refresh_feeds.py
│   └── utils
│       ├── __init__.py
│       ├── base_model.py
│       └── base_repository.py
├── conftest.py
├── docker-compose.yml
├── mypy.ini
├── pytest.ini
├── readme.md
├── requirements.txt
├── testdbconfig.py
└── tests
    ├── __init__.py
    ├── factories.py
    ├── mock_responses.py
    ├── test_apis
    │   ├── test.db
    │   ├── test_feeds.py
    │   └── test_posts.py
    └── test_services
        └── test_rss_feed_services
            ├── test_feed_creator.py
            ├── test_feed_fetcher.py
            └── test_feed_updater.py
````

# Installation
To install and run the RSS feed service using Docker Compose, follow these steps:

1. Create a new file named `.env` from `.env.example` using a text editor:
```bash
cp .env.example .env
```

2. Open the .env file in a text editor and define the necessary environment variables. 
These variables are used to configure the application. You can use the following content
```bash
SECRET_KEY=43289e6b7d669e15ae00f54abcdf8a9f
DATABASE_URL=postgresql+psycopg2://admin:password@rssfeed_db:5432/rssfeed_db
DB_USER=admin
DB_PASSWORD=password
DB_NAME=rssfeed_db
TEST_DB_NAME=test_rssfeed_db
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672/
CELERY_RESULT_BACKEND=rpc://
```

3. Build and start the Docker containers using Docker Compose:
```bash
docker-compose up -d
```
This command will build the Docker image and start the containers in detached mode.

4. Verify that the containers are running:
```bash
docker-compose ps
```
You should see the running containers listed, including the RSS feed service container.

4. Now run the migrations using alembic in docker container:
```bash
docker-compose run --rm api alembic upgrade head
```

6. The RSS feed service will now be accessible at http://localhost:8000.
- To access API doc: http://localhost:8000/docs
- To access pgadmin: http://127.0.0.1:5050/

## API Endpoints
The RSS feed service provides the following API endpoints:
- /auth/register - Register a new user. [POST]
- /auth/login - Log in and obtain an access token. [POST]
- /feeds - Get a list of all feeds. [GET]
- /feeds - Allow a user to create a new feed. [POST]
- /feeds/{feed_id}/force-refresh  - Allow a user to force-refresh a specific feed. [POST]
- /feeds/{feed_id}/follow  - Allow a user to follow a specific feed. [POST]
- /feeds/{feed_id}/follow  - Allow a user to unfollow a specific feed. [DELETE]
- /posts/{post_id} - Get a list of  posts of a following feed. [GET]
- /posts/{post_id}/mark - mark/un-mark read status of a post. [PUT]

You can use tools like cURL, Postman, or any other HTTP client to interact with the API endpoints.

# Code Quality and Standards
### Code Linting
Check `app` linting 
```bash
ruff app
````

To fix linting issues
```bash
ruff --fix app
````

### Typing
```bash
mypy app
````



# Run Tests
Run the tests using pytest in docker:
```bash
docker-compose run --rm api pytest
```
This command will discover and execute all the tests in the project.

If you want to generate a coverage report to see the test coverage, 
you can use the --cov option:

```bash
docker-compose run --rm api pytest --cov=app
```
The coverage report will show which parts of the code are covered by the tests.

Current the test coverage is 79%
```bash
---------- coverage: platform linux, python 3.9.17-final-0 -----------
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
app/__init__.py                                      0      0   100%
app/api/__init__.py                                  0      0   100%
app/api/auth.py                                     20      8    60%
app/api/feeds.py                                    40      8    80%
app/api/posts.py                                    23      0   100%
app/auth/__init__.py                                 0      0   100%
app/auth/constants.py                                1      0   100%
app/auth/jwt_bearer.py                              15      3    80%
app/auth/jwt_handler.py                             33      5    85%
app/auth/service.py                                 14      0   100%
app/celery_app.py                                   10      0   100%
app/config.py                                       12      0   100%
app/constants.py                                     5      0   100%
app/database.py                                     13      4    69%
app/main.py                                         18      0   100%
app/models.py                                       44      0   100%
app/repositories/__init__.py                         0      0   100%
app/repositories/feed_repository.py                 16      1    94%
app/repositories/post_repository.py                 26      3    88%
app/repositories/user_repository.py                 18      5    72%
app/schemas.py                                      50      0   100%
app/services/__init__.py                             0      0   100%
app/services/auth_service.py                        28     18    36%
app/services/feed_manager_service.py                18     10    44%
app/services/feed_service.py                        69     30    57%
app/services/post_service.py                        37      4    89%
app/services/rss_feed_services/__init__.py           3      0   100%
app/services/rss_feed_services/feed_creator.py      56     12    79%
app/services/rss_feed_services/feed_fetcher.py      18      0   100%
app/services/rss_feed_services/feed_updater.py      46      5    89%
app/services/user_service.py                         7      3    57%
app/tasks/__init__.py                                4      0   100%
app/tasks/fetch_and_assign_feed_to_user.py          16      6    62%
app/tasks/force_refresh_feed.py                     11      4    64%
app/tasks/refresh_feed.py                           26     18    31%
app/tasks/refresh_feeds.py                          14      5    64%
app/utils/__init__.py                                0      0   100%
app/utils/base_model.py                              7      0   100%
app/utils/base_repository.py                         5      0   100%
--------------------------------------------------------------------
TOTAL                                              723    152    79%
```

## Areas for Improvement
### Backend
- Ensure that the application is free from typing errors. 
Currently, there are few remaining `mypy` errors that need to be resolved.
- To optimize performance, utilize the asynchronous query mechanism in SQLAlchemy and incorporate more asynchronous operations throughout the application.

### Testing
- Increase test coverage by adding more unit tests and integration tests.
Specially for services, repositories, and tasks.

## Assumptions
- When a user follows a feed and performs a force-refresh, 
the changes will be reflected for all other users who are also following the same feed.
- If a feed is currently on a back-off mechanism and a user attempts to force-refresh,
the force-refresh will be allowed only after the back-off mechanism has completed.
- Every 5 minutes, a 'refresh_feeds' task is scheduled, 
which in turn spawns 'refresh_feed' Celery tasks to individually refresh each feed.
- Still using sqlite for the tests.

## Database ERD
![Database ERD](./documentations/assets/rss-feed-service-erd.png)