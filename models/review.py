from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .movie import Movie
    from .user import User

class Review(SQLModel, table=True):
    id_review: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id_movie", nullable=False)
    user_id: int = Field(foreign_key="user.id_user", nullable=False)  # CORRIGIDO: estava movie.id_user
    rating: float = Field(nullable=False)
    content: Optional[str] = Field(default=None, nullable=True)

    movie: "Movie" = Relationship(back_populates="reviews")
    user: "User" = Relationship(back_populates="reviews")