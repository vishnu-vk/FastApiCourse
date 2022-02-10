from app import schemas

def test_votes_up(authorized_client,test_post):
    response = authorized_client.post("/votes/", json= {"post_id": test_post[0].id, "dir": True})
    assert response.status_code == 201

def test_votes_down(authorized_client,test_post):
    response = authorized_client.post("/votes/", json= {"post_id": test_post[0].id, "dir": False})
    assert response.status_code == 404

def test_votes_unauthorized(client,test_post):
    response = client.post("/votes/", json= {"post_id": test_post[0].id, "dir": True})
    assert response.status_code == 401

def test_votes_post_not_exits(authorized_client,test_post):
    response = authorized_client.post("/votes/", json= {"post_id": 666, "dir": False})
    assert response.status_code == 404