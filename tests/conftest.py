from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




@pytest.fixture()
def session():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello66@test.com", "password": "new"}
    response = client.post("/users/", json= user_data)
    new_user = response.json()
    new_user['password'] = user_data["password"]
    assert response.status_code == 201
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_post(test_user, session):
    post_data = [
        {"title": 'title 1', "content": 'content 1', "published": True, "owner_id": test_user['id']},
        {"title": 'title 2', "content": 'content 2', "published": None, "owner_id": test_user['id']},
        {"title": 'title 3', "content": 'content 3', "published": None, "owner_id": test_user['id']},
        {"title": 'title 4', "content": 'content 4', "published": False, "owner_id": test_user['id']},
        {"title": 'title 5', "content": 'content 5', "published": None, "owner_id": test_user['id']}
        ]

    posts = list(map(lambda post: models.Post(**post), post_data))

    session.add_all(posts)
    session.commit()
    return posts
