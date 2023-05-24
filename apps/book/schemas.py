from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int | None
    name: str
    author_id: int

    class Config:
        orm_mode = True

class BookAuthorSchema(BookSchema):
    author: "AuthorSchema"

from apps.author.schemas import AuthorSchema
BookAuthorSchema.update_forward_refs()
