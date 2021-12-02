from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from core.posts.schemas import *
from core.posts.managers import *
from core.posts.models import *
from core.posts.exceptions import *
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.post(
    '/new',
    response_model=BlogPostOutSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_blog_post(request: BlogPostCreateSchema, manager: BlogPostManager = Depends()):
    instance = await manager.create_blog_post(request)
    return instance


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_blog_post(id: int, manager: BlogPostManager = Depends()):
    try:
        instance = await manager.get_post_by_id(id)
        # permission check
    except BlogNotFound:
        return
        
    await manager.delete_blog_post(instance)


@router.get(
    '/list',
    response_model=List[BlogPostOutSchema]
)
async def get_post_list(manager: BlogPostManager = Depends()):
    return await manager.get_posts()


@router.get(
    '/list/{user_id}',
    response_model=List[BlogPostOutSchema]
)
async def get_posts_by_user_id(user_id: UUID, manager: BlogPostManager = Depends()):
    filters = {
        "creator_id": user_id
    }
    return await manager.get_posts(filters)


@router.get(
    '/tags/list',
    response_model=List[TagSchema]
)
async def get_tag_list(manager: TagManager = Depends()):
    return await manager.get_tag_list()


@router.get(
    '/tags/{name}',
    response_model=List[BlogPostOutSchema]
)
async def get_posts_in_tag(name: str, manager: TagManager = Depends()):
    try:
        posts = await manager.get_posts_in_tag(name)
    except TagNotFound as e:
        raise HTTPException(404, detail=e.details)
    
    return posts