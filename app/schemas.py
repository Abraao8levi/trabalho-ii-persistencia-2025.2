from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel


# Review Schemas
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

# Watchlist Schemas
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

# Aggregation Schemas
class MovieStats(SQLModel):
    movie_id: int
    movie_title: str
    avg_rating: float
    review_count: int
    watchlist_count: int

class UserActivity(SQLModel):
    user_id: int
    user_name: str
    reviews_count: int
    watchlist_count: int
    avg_user_rating: float

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


class GenreBase(SQLModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id_genre: int

class GenreUpdate(SQLModel):
    name: Optional[str] = None

class UserBase(SQLModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id_user: int
    created_at: datetime

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

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