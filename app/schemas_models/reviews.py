from typing import Optional
from sqlmodel import SQLModel


class ReviewBase(SQLModel):
    movie_id: int
    user_id: int
    rating: float
    content: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(SQLModel):
    rating: Optional[float] = None
    content: Optional[str] = None


class ReviewRead(ReviewBase):
    id_review: int


class ReviewWithRelations(ReviewRead):
    movie_title: Optional[str] = None
    user_name: Optional[str] = None
