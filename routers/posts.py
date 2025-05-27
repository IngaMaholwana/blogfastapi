from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.PostOut)
def create_post(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a new blog post.

    Args:
        user_id (int): The ID of the user creating the post.
        post (schemas.PostCreate): The data for the new post (title, content).
        db (Session): The database session dependency.

    Returns:
        schemas.PostOut: The created post with its details.

    This function takes the user ID and post data, creates a new `Post` object,
    saves it to the database, and returns the created post.
    """
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[schemas.PostOut])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of blog posts with pagination.

    Args:
        skip (int): The number of posts to skip (default: 0).
        limit (int): The maximum number of posts to return (default: 10).
        db (Session): The database session dependency.

    Returns:
        list[schemas.PostOut]: A list of posts with their details.

    This function queries the database for posts, including their owners,
    and returns a paginated list of posts.
    """
    posts = db.query(models.Post).options(joinedload(models.Post.owner)).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=schemas.PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single blog post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.
        db (Session): The database session dependency.

    Returns:
        schemas.PostOut: The details of the requested post.

    Raises:
        HTTPException: If the post with the given ID is not found.

    This function queries the database for a post by its ID, including its owner,
    and returns the post details if found.
    """
    post = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Update an existing blog post.

    Args:
        post_id (int): The ID of the post to update.
        post (schemas.PostCreate): The new data for the post (title, content).
        db (Session): The database session dependency.

    Returns:
        schemas.PostOut: The updated post with its details.

    Raises:
        HTTPException: If the post with the given ID is not found.

    This function retrieves a post by its ID, updates its fields with the new data,
    saves the changes to the database, and returns the updated post.
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", response_model=schemas.PostOut)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a blog post by its ID.

    Args:
        post_id (int): The ID of the post to delete.
        db (Session): The database session dependency.

    Returns:
        schemas.PostOut: The details of the deleted post.

    Raises:
        HTTPException: If the post with the given ID is not found.

    This function retrieves a post by its ID, deletes it from the database,
    and returns the details of the deleted post.
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return db_post

@router.get("/search/", response_model=list[schemas.PostOut])
def search_posts(query: str, db: Session = Depends(get_db)):
    """
    Search for blog posts by title or content.

    Args:
        query (str): The search query string.
        db (Session): The database session dependency.

    Returns:
        list[schemas.PostOut]: A list of posts matching the search query.

    This function queries the database for posts where the title or content
    contains the search query and returns the matching posts.
    """
    posts = db.query(models.Post).filter(models.Post.title.contains(query) | models.Post.content.contains(query)).all()
    return posts