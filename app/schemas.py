from typing import Optional, List
from sqlmodel import SQLModel
from datetime import datetime

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