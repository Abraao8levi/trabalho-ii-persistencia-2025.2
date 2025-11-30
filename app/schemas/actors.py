from typing import Optional
from sqlmodel import SQLModel


class ActorBase(SQLModel):
    name: str
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None


class ActorCreate(ActorBase):
    pass


class ActorRead(ActorBase):
    id_actor: int


class ActorUpdate(SQLModel):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None
