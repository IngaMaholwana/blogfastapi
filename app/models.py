from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    """
    Database model for users.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user, must be unique.
        email (str): The email address of the user, must be unique.
        password (str): The hashed password of the user.

    Relationships:
        posts (list[Post]): A list of posts created by the user.
        comments (list[Comment]): A list of comments authored by the user.

    This model represents the `users` table in the database. It defines the
    columns and relationships for storing user data.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    """
    Database model for blog posts.

    Attributes:
        id (int): The unique identifier for the post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        created_at (datetime): The timestamp when the post was created.
        owner_id (int): The ID of the user who owns the post.

    Relationships:
        owner (User): The user who created the post.
        comments (list[Comment]): A list of comments associated with the post.

    This model represents the `posts` table in the database. It defines the
    columns and relationships for storing blog post data.
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    """
    Database model for comments.

    Attributes:
        id (int): The unique identifier for the comment.
        content (str): The content of the comment.
        post_id (int): The ID of the post to which the comment belongs.
        author_id (int): The ID of the user who authored the comment.

    Relationships:
        post (Post): The blog post to which the comment belongs.
        author (User): The user who authored the comment.

    This model represents the `comments` table in the database. It defines the
    columns and relationships for storing comment data.
    """
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")