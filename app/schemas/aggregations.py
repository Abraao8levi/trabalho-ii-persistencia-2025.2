from sqlmodel import SQLModel


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
