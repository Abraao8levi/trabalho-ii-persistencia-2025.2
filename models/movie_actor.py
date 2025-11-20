from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional

class MovieActor(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id_movie", primary_key=True)
    actor_id: Optional[int] = Field(default=None, foreign_key="actor.id_actor", primary_key=True)