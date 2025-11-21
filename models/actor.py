from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .movie import Movie

class Actor(SQLModel, table=True):
    __tablename__ = "actor"
    
    id_actor: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    birth_date: Optional[str] = Field(default=None, nullable=True)
    nationality: Optional[str] = Field(default=None, nullable=True)
    biography: Optional[str] = Field(default=None, nullable=True)

    # Relação N:N com Movie através da tabela associativa MovieActor
    movies: List["Movie"] = Relationship(
        back_populates="actors", 
        link_model="MovieActor"  # Usando string para evitar circular imports
    )