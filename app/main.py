from fastapi import FastAPI
from .routers import posts
import time
from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(posts.router)

import psycopg2
from psycopg2.extras import RealDictCursor
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='ff-pa', user='postgres', password='000001', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def read_root():
    return {"data": "Hello"}

@app.get("/sql")
def test_post():

    return {"data": "nice"}