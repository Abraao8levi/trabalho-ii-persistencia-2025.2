from datetime import date
from typing import Optional
from sqlmodel import SQLModel


class MovieBase(SQLModel):
    title: str
    synopsis: Optional[str] = None
    release_date: date
    duration_minutes: int
    age_rating: Optional[str] = None
    director: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    id_movie: int


class MovieUpdate(SQLModel):
    title: Optional[str] = None
    synopsis: Optional[str] = None
    release_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    age_rating: Optional[str] = None
    director: Optional[str] = None
