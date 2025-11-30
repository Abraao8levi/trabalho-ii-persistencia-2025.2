from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from models.models import Movie
from app.schemas_models.movies import MovieCreate, MovieUpdate, MovieRead
from app.schemas_models.actors import ActorRead
from app.schemas_models.genres import GenreRead
from app.schemas_models.aggregations import MovieFullInfo
from app.crud.exceptions import NotFoundException


def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
    """
    Retorna um filme pelo seu ID.
    """
    return db.get(Movie, movie_id)


def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
    """
    Retorna uma lista de filmes com paginação.
    """
    statement = select(Movie).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_movie(db: Session, movie: MovieCreate) -> Movie:
    """
    Cria um novo filme no banco de dados.
    """
    db_movie = Movie.model_validate(movie)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db: Session, movie_id: int, movie_update: MovieUpdate) -> Optional[Movie]:
    """
    Atualiza as informações de um filme existente.
    """
    db_movie = db.get(Movie, movie_id)
    if not db_movie:
        return None
    movie_data = movie_update.model_dump(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int) -> Optional[Movie]:
    """
    Deleta um filme do banco de dados.
    """
    db_movie = db.get(Movie, movie_id)
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie

def get_movie_full_info(db: Session, movie_id: int) -> MovieFullInfo:
    statement = (
        select(Movie)
        .where(Movie.id_movie == movie_id)
        .options(
            joinedload(Movie.actors),
            joinedload(Movie.genres),
            joinedload(Movie.reviews)
        )
    )

    movie = db.exec(statement).first()

    if not movie:
        raise NotFoundException("Movie not found")
    
    return MovieFullInfo(
        movie=MovieRead.model_validate(movie),
        actors=[ActorRead.model_validate(a) for a in movie.actors],
        genres=[GenreRead.model_validate(g) for g in movie.genres],
        review_count=len(movie.reviews)
    )