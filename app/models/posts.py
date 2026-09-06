import datetime
from typing import Optional, List, Annotated
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class PostModel(BaseModel):
    """
    Container for a single post record.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    short: str = Field(...)
    poster: str | None  = None
    createdAt: datetime = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Jane Doe",
                "short": "jdoe@example.com",
                "poster": "http://example.com/post.jpg",
            }
        },
    )

class PostsCollection(BaseModel):
    """
    A container holding a list of `PostsModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    posts: List[PostModel]
