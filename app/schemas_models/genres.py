from typing import Optional
from sqlmodel import SQLModel


class GenreBase(SQLModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreRead(GenreBase):
    id_genre: int


class GenreUpdate(SQLModel):
    name: Optional[str] = None
