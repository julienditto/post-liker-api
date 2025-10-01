from typing import List
from app import schemas
import pytest
from app import schemas

def test_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("title1", "content1", True),
    ("title2", "content2", True),
    ("title3", "content3", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, 
                                                  "published": published})
    created_post = schemas.PostReturn(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={"title": "title", "content": "content"})
    created_post = schemas.PostReturn(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

def test_unauthorized_create_post(client):
    res = client.post("/posts/", json={"title": "title", "content": "content", 
                                                  "published": "published"})
    assert res.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
