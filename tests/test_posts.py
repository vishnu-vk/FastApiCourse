import pytest

from app import schemas

def test_get_all_posts(authorized_client, test_post):
    response = authorized_client.get("/posts/")
    posts = list(map(lambda apost: schemas.PostOut(**apost) ,response.json()))
    assert response.status_code == 200
    assert len(response.json()) == len(test_post)

def test_get_all_posts_unathorized(client, test_post):
    response = client.get("/posts/") 
    assert response.status_code == 401


def test_get_one_posts_unathorized(client, test_post):
    response = client.get(f"/posts/{test_post[0].id}") 
    assert response.status_code == 401

def test_get_one_posts(authorized_client, test_post):
    response = authorized_client.get(f"/posts/{test_post[0].id}") 
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_post[0].id
    assert post.Post.title == test_post[0].title
    assert post.Post.content == test_post[0].content

def test_get_one_posts_not_exits(authorized_client, test_post):
    response = authorized_client.get("/posts/99") 
    assert response.status_code == 404

@pytest.mark.parametrize("title, content, published, status_code",[
    ("title 1", "content 1", False, 201),
    ("title 2", "content 2", True, 201),
    ("title 3", "content 3", None, 422),
    ("title 4", None, False, 422),
    (None, "content 5", False, 422),
    (None, None, None, 422)
])
def test_create_posts(authorized_client, title, content, published, status_code):
    response = authorized_client.post("/posts/",json={"title": title, "content": content, "published": published, "owner_id": 1})
    assert response.status_code == status_code
    if(status_code == 201):
        post = schemas.PostResponse(**response.json())


def test_create_posts_unauthorized(client):
    response = client.post("/posts/",json={"title": "title 1", "content": "content 1"})
    assert response.status_code == 401

def test_update_posts_unauthorized(client, test_post):
    response = client.put("/posts/1",json={"title": "title 1", "content": "content 1"})
    assert response.status_code == 401

def test_update_posts_not_exits(authorized_client, test_post):
    response = authorized_client.put("/posts/99",json={"title": "title 1", "content": "content 1"})
    assert response.status_code == 404

def test_update_post(authorized_client, test_post):
    response = authorized_client.put("/posts/1",json={"title": "title 1", "content": "content 1"})
    post = schemas.PostResponse(**response.json())
    assert response.status_code == 200


def test_delete_post(authorized_client, test_post):
    response = authorized_client.delete("/posts/1")
    assert response.status_code == 204

def test_delete_post_not_exits(authorized_client, test_post):
    response = authorized_client.delete("/posts/99")
    assert response.status_code == 404

def test_delete_post_unathorized(client, test_post):
    response = client.delete("/posts/1")
    assert response.status_code == 401