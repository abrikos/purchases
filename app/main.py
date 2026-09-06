from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from app.routers import posts, auth

load_dotenv()


app = FastAPI()
app.include_router(posts.router)
app.include_router(auth.router)


@app.get("/",  response_class=HTMLResponse)
def read_root():
    return ""


# @app.post(
#     "/posts/",
#     response_description="Add new student",
#     response_model=PostModel,
#     status_code=status.HTTP_201_CREATED,
#     response_model_by_alias=False,
# )
# async def create_post(student: PostModel = Body(...)):
#     """
#     Insert a new student record.
#
#     A unique `id` will be created and provided in the response.
#     """
#     new_post = student.model_dump(by_alias=True, exclude=["id"])
#     result = await post_collection.insert_one(new_post)
#     new_post["_id"] = result.inserted_id
#     new_post["detail"] = "result.inserted_id2222"
#
#     return new_post

@app.get("/profile/")
async def read_profile():
    return {"id": "111", "email": "aaa@aaa.com"}
