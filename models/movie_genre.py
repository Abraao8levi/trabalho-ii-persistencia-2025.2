from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional

class MovieGenre(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id_movie", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id_genre", primary_key=True)