from typing import Optional
from sqlmodel import SQLModel


class WatchlistBase(SQLModel):
    id_user: int
    id_movie: int
    notes: Optional[str] = None


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistUpdate(SQLModel):
    notes: Optional[str] = None


class WatchlistRead(WatchlistBase):
    id_watchlist: int


class WatchlistWithRelations(WatchlistRead):
    movie_title: Optional[str] = None
    user_name: Optional[str] = None
