from typing import Union
from fastapi import APIRouter, status, Response, HTTPException, Depends
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
import random

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

my_posts = [{"title": "title of post 1", "content": "content 1", "id": 1},
            {"title": "ok post2", "content": "content 2", "id": 2}]

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@router.get("", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(data: schemas.Post, db: Session = Depends(get_db)):
    # title=data.title, content=data.content, published=data.published
    new_post = models.Post(**data.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, data: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not exist")
    
    post_query.update(data.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}