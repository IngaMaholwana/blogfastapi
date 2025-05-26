from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Post
from app.schemas import PostCreate, PostOut
from app.database import get_db

def test_create_post(db: Session):
    post_data = PostCreate(title="Test Post", content="This is a test post.")
    response = create_post(post_data, db)
    assert response.title == post_data.title
    assert response.content == post_data.content

def test_read_post(db: Session):
    post = db.query(Post).first()
    response = read_post(post.id, db)
    assert response.id == post.id
    assert response.title == post.title

def test_update_post(db: Session):
    post = db.query(Post).first()
    updated_data = PostCreate(title="Updated Title", content="Updated content.")
    response = update_post(post.id, updated_data, db)
    assert response.title == updated_data.title
    assert response.content == updated_data.content

def test_delete_post(db: Session):
    post = db.query(Post).first()
    response = delete_post(post.id, db)
    assert response.id == post.id
    assert db.query(Post).filter(Post.id == post.id).first() is None

def test_search_posts(db: Session):
    search_query = "Test"
    response = search_posts(search_query, db)
    assert len(response) > 0
    for post in response:
        assert search_query in post.title or search_query in post.content