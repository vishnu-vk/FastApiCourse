from jose import jwt
from app.config import settings
from app import schemas

import pytest

def test_create_user(client):
    response = client.post("/users/", json={"email": "hello@test.com", "password": "new"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "hello@test.com"
    assert response.status_code == 201

def test_get_all_user(client):
    response = client.get("/users/")
    assert response.status_code == 200

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    response_token = schemas.AccessToken(**response.json())
    payload = jwt.decode(response_token.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert response_token.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ('hello66@test.com', 'new', 200),
    ('wrongemail@gmail.com', 'new', 403),
    ('hello66@test.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'new', 422),
    ('hello66@test.com', None, 422)
])
def test_invalid_login_user(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code

