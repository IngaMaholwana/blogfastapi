from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User-related schemas

class UserBase(BaseModel):
    """
    Base schema for user-related data.

    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user, validated as a proper email format.

    This schema is used as a base for other user-related schemas.
    """
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        password (str): The password for the user.

    This schema extends `UserBase` and adds a password field for user registration.
    """
    password: str

class UserOut(BaseModel):
    """
    Schema for returning user data in responses.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.

    This schema is used to serialize user data for responses, excluding sensitive fields like the password.
    """
    id: int
    email: str
    class Config:
        from_attributes = True  # Enables compatibility with ORM models.

# Post-related schemas

class PostBase(BaseModel):
    """
    Base schema for blog post-related data.

    Attributes:
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    This schema is used as a base for other post-related schemas.
    """
    title: str
    content: str

class PostCreate(PostBase):
    """
    Schema for creating a new blog post.

    This schema inherits all fields from `PostBase` and is used for validating
    data when creating a new blog post.
    """
    pass

class PostOut(BaseModel):
    """
    Schema for returning blog post data in responses.

    Attributes:
        id (int): The unique identifier of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        created_at (datetime): The timestamp when the blog post was created.
        owner (UserOut): The user who created the blog post.

    This schema is used to serialize blog post data for responses, including the owner details.
    """
    id: int
    title: str
    content: str
    created_at: datetime
    owner: UserOut
    class Config:
        from_attributes = True  # Enables compatibility with ORM models.

# Comment-related schemas

class CommentCreate(BaseModel):
    """
    Schema for creating a new comment.

    Attributes:
        content (str): The content of the comment.

    This schema is used for validating data when creating a new comment.
    """
    content: str

class CommentOut(BaseModel):
    """
    Schema for returning comment data in responses.

    Attributes:
        id (int): The unique identifier of the comment.
        content (str): The content of the comment.
        author (UserOut): The user who authored the comment.

    This schema is used to serialize comment data for responses, including the author details.
    """
    id: int
    content: str
    author: UserOut
    class Config:
        from_attributes = True  # Enables compatibility with ORM models.