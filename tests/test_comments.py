from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

def test_create_comment(db: Session):
    # Create a user
    user = models.User(username="testuser", email="test@example.com", password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create a post
    post = models.Post(title="Test Post", content="This is a test post.", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)

    # Create a comment
    comment_data = schemas.CommentCreate(content="This is a test comment.")
    comment = models.Comment(content=comment_data.content, post_id=post.id, author_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    assert comment.content == comment_data.content
    assert comment.post_id == post.id
    assert comment.author_id == user.id

def test_get_comments(db: Session):
    # Assuming a comment already exists
    comment = db.query(models.Comment).first()
    assert comment is not None

    # Retrieve comments for a specific post
    comments = db.query(models.Comment).filter(models.Comment.post_id == comment.post_id).all()
    assert len(comments) > 0

def test_delete_comment(db: Session):
    # Create a user and a post
    user = models.User(username="testuser", email="test@example.com", password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)

    post = models.Post(title="Test Post", content="This is a test post.", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)

    # Create a comment
    comment = models.Comment(content="This is a test comment.", post_id=post.id, author_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    # Delete the comment
    db.delete(comment)
    db.commit()

    # Verify the comment is deleted
    deleted_comment = db.query(models.Comment).filter(models.Comment.id == comment.id).first()
    assert deleted_comment is None