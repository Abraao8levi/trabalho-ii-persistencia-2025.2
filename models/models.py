# models.py
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from datetime import date, datetime

if TYPE_CHECKING:
    from .models import Movie, Review, Watchlist, Actor, Genre



# Tabela de junção para Movie-Actor (many-to-many)
class MovieActor(SQLModel, table=True):
    __tablename__ = "movie_actor"
    
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id_movie", primary_key=True)
    actor_id: Optional[int] = Field(default=None, foreign_key="actor.id_actor", primary_key=True)


# Tabela de junção para Movie-Genre (many-to-many)
class MovieGenre(SQLModel, table=True):
    __tablename__ = "movie_genre"
    
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id_movie", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id_genre", primary_key=True)


class Actor(SQLModel, table=True):
    __tablename__ = "actor"

    id_actor: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    birth_date: Optional[str] = Field(default=None)
    nationality: Optional[str] = Field(default=None)
    biography: Optional[str] = Field(default=None)

    movies: List["Movie"] = Relationship(
        back_populates="actors",
        link_model=MovieActor
    )


class Genre(SQLModel, table=True):
    __tablename__ = "genre"

    id_genre: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)

    movies: List["Movie"] = Relationship(
        back_populates="genres",
        link_model=MovieGenre
    )



class Movie(SQLModel, table=True):
    __tablename__ = "movie"

    id_movie: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True)
    synopsis: Optional[str] = Field(default=None)
    release_date: date = Field(nullable=False)
    duration_minutes: int = Field(nullable=False)
    age_rating: Optional[str] = Field(default=None)
    director: Optional[str] = Field(default=None)

    reviews: List["Review"] = Relationship(back_populates="movie")
    watchlists: List["Watchlist"] = Relationship(back_populates="movie")

    genres: List["Genre"] = Relationship(
        back_populates="movies",
        link_model=MovieGenre
    )
    actors: List["Actor"] = Relationship(
        back_populates="movies",
        link_model=MovieActor
    )


class User(SQLModel, table=True):
    __tablename__ = "user"

    id_user: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False, index=True, max_length=50)
    email: str = Field(unique=True, nullable=False, index=True, max_length=255)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    reviews: List["Review"] = Relationship(back_populates="user")
    watchlists: List["Watchlist"] = Relationship(back_populates="user")



class Review(SQLModel, table=True):
    __tablename__ = "review"

    id_review: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id_movie", nullable=False)
    user_id: int = Field(foreign_key="user.id_user", nullable=False)
    rating: float = Field(nullable=False)
    content: Optional[str] = Field(default=None)

    movie: "Movie" = Relationship(back_populates="reviews")
    user: "User" = Relationship(back_populates="reviews")



class Watchlist(SQLModel, table=True):
    __tablename__ = "watchlist"

    id_watchlist: Optional[int] = Field(default=None, primary_key=True)
    notes: Optional[str] = Field(default=None)
    id_user: int = Field(foreign_key="user.id_user", nullable=False)
    id_movie: int = Field(foreign_key="movie.id_movie", nullable=False)

    user: "User" = Relationship(back_populates="watchlists")
    movie: "Movie" = Relationship(back_populates="watchlists")