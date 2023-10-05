from typing import Union
from fastapi import APIRouter, status, Response, HTTPException
from .. import schemas
import random

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

my_posts = [{"title": "title of post 1", "content": "content 1", "id": 1},
            {"title": "ok post2", "content": "content 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@router.get("", status_code=status.HTTP_200_OK)
def get_posts():
    return {"data": my_posts}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(data: schemas.Post):
    post_dict = data.model_dump()
    post_dict['id'] = random.randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, post: schemas.Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not exist")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return {"data": post_dict}