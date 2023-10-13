from fastapi import FastAPI
from .routers import posts, users
import time
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"data": "Hello"}