import os


from dotenv import load_dotenv
from fastapi import FastAPI, status, Body, Request, Response
from pymongo import AsyncMongoClient
from starlette.responses import HTMLResponse
from models.posts import PostsCollection, PostModel
from routers import posts

app.include_router(users.router)
load_dotenv()


app = FastAPI()
client = AsyncMongoClient(os.environ["MONGODB_URL"])
db = client.abrikoz
post_collection = db.get_collection("posts")

@app.get("/",  response_class=HTMLResponse)
def read_root():
    return ""


# @app.get(
#     "/posts/",
#     response_description="List all posts",
#     response_model=list[PostModel],
#     response_model_by_alias=False
# )
# async def list_posts():
#     """
#     List all of the student data in the database.
#
#     The response is unpaginated and limited to 1000 results.
#     """
#     return await post_collection.find().sort('createdAt', -1).to_list(1000)
#     #return PostsCollection(posts=await post_collection.find().sort('createdAt', -1).to_list(1000))

@app.post(
    "/posts/",
    response_description="Add new student",
    response_model=PostModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_post(student: PostModel = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_post = student.model_dump(by_alias=True, exclude=["id"])
    result = await post_collection.insert_one(new_post)
    new_post["_id"] = result.inserted_id
    new_post["detail"] = "result.inserted_id2222"

    return new_post

@app.get("/profile/")
async def read_profile():
    return {"id": "111", "email": "aaa@aaa.com"}
