from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

# Create a router for comment-related endpoints
router = APIRouter()

@router.post("/", response_model=schemas.CommentOut)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    """
    Create a new comment for a specific blog post.

    Args:
        post_id (int): The ID of the post to which the comment belongs.
        comment (schemas.CommentCreate): The data for the new comment (content).
        db (Session): The database session dependency.

    Returns:
        schemas.CommentOut: The created comment with its details.

    This function creates a new `Comment` object, associates it with the specified post,
    saves it to the database, and returns the created comment. The `post_id` is used to
    link the comment to the corresponding blog post.
    """
    db_comment = models.Comment(content=comment.content, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{post_id}", response_model=list[schemas.CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all comments for a specific blog post.

    Args:
        post_id (int): The ID of the post for which to retrieve comments.
        db (Session): The database session dependency.

    Returns:
        list[schemas.CommentOut]: A list of comments associated with the specified post.

    This function queries the database for all comments linked to the given `post_id`
    and returns them as a list. If no comments are found, an empty list is returned.
    """
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments