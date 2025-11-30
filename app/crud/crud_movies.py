from typing import List, Optional

from sqlmodel import Session, select

from ... import models, schemas


def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    """
    Retorna um filme pelo seu ID.
    """
    return db.get(models.Movie, movie_id)


def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Movie]:
    """
    Retorna uma lista de filmes com paginação.
    """
    statement = select(models.Movie).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_movie(db: Session, movie: schemas.MovieCreate) -> models.Movie:
    """
    Cria um novo filme no banco de dados.
    """
    db_movie = models.Movie.model_validate(movie)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db: Session, movie_id: int, movie_update: schemas.MovieUpdate) -> Optional[models.Movie]:
    """
    Atualiza as informações de um filme existente.
    """
    db_movie = db.get(models.Movie, movie_id)
    if not db_movie:
        return None
    movie_data = movie_update.model_dump(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    """
    Deleta um filme do banco de dados.
    """
    db_movie = db.get(models.Movie, movie_id)
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie
