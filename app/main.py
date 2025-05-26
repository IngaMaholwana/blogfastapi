from fastapi import FastAPI
from app import models
from app.database import engine
from routers import users, posts, comments

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)