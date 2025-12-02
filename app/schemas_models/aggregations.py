from sqlmodel import SQLModel
from typing import List
from .movies import MovieRead
from .actors import ActorRead
from .genres import GenreRead
from .reviews import ReviewRead

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

class MovieFullInfo(SQLModel):
    movie: MovieRead
    actors: List[ActorRead]
    genres: List[GenreRead]
    reviews: List[ReviewRead]
    review_count: int