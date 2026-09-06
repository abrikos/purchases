from fastapi import APIRouter

from app.db import db
from app.models.posts import PostModel

router = APIRouter(prefix="/posts", tags=["posts"], responses={404: {"description": "Not found"}},)
post_collection = db.get_collection("posts")

@router.get(
    "/",
    response_description="List all posts",
    response_model=list[PostModel],
    response_model_by_alias=False
)
async def list_posts():
    """
    List all of the student data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return await post_collection.find().sort('createdAt', -1).to_list(1000)
    #return PostsCollection(posts=await post_collection.find().sort('createdAt', -1).to_list(1000))
