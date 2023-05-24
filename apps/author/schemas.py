from pydantic import BaseModel


class AuthorSchema(BaseModel):
    id: int | None
    name: str

    class Config:
        orm_mode = True

class AuthorBookSchema(AuthorSchema):
    books: list["BookSchema"]

from apps.book.schemas import BookSchema
AuthorBookSchema.update_forward_refs()