from fastapi import FastAPI
from app import models
from app.database import engine
from routers import users, posts, comments

# Create all database tables
models.Base.metadata.create_all(bind=engine)
"""
This line ensures that all database tables defined in the ORM models are created.
- `models.Base.metadata`: Contains metadata for all ORM models.
- `create_all(bind=engine)`: Creates the tables in the database if they do not already exist.
- `engine`: The database connection engine used to execute the table creation commands.
"""

# Initialize the FastAPI application
app = FastAPI()
"""
The `app` object is an instance of the FastAPI class.
- It serves as the main entry point for the application.
- Routes, middleware, and other configurations are added to this object.
"""

# Include the user-related routes
app.include_router(users.router)
"""
This line includes the routes defined in the `users` router.
- `users.router`: The router object from the `routers/users.py` file.
- All endpoints related to user operations (e.g., registration, login) are added to the application.
"""

# Include the post-related routes
app.include_router(posts.router)
"""
This line includes the routes defined in the `posts` router.
- `posts.router`: The router object from the `routers/posts.py` file.
- All endpoints related to blog post operations (e.g., create, read, update, delete) are added to the application.
"""

# Include the comment-related routes
app.include_router(comments.router)
"""
This line includes the routes defined in the `comments` router.
- `comments.router`: The router object from the `routers/comments.py` file.
- All endpoints related to comment operations (e.g., add, retrieve) are added to the application.
"""