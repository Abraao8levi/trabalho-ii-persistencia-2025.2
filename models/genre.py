from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .movie import Movie

class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    
    id_genre: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)

    # Relação N:N com Movie através da tabela associativa MovieGenre
    movies: List["Movie"] = Relationship(
        back_populates="genres", 
        link_model="MovieGenre"  # Usando string para evitar circular imports
    )