# app/routers/movies.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date
from app.database import get_session
from models.models import Movie
from app.schemas import MovieCreate, MovieRead, MovieUpdate

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.post("/", response_model=MovieRead)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie



@router.get("/", response_model=List[Movie])
def get_movies(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
):
    movies = session.exec(select(Movie).offset(offset).limit(limit)).all()
    return movies




@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie



@router.put("/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie_update: Movie, session: Session = Depends(get_session)):
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_data = movie_update.model_dump(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie



@router.delete("/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    session.delete(movie)
    session.commit()
    return {"message": "Movie deleted successfully"}


@router.get("/search/{title}", response_model=List[Movie])
def search_movies_by_title(
    title: str,
    session: Session = Depends(get_session)
):
    statement = select(Movie).where(Movie.title.ilike(f"%{title}%"))
    movies = session.exec(statement).all()
    return movies



@router.get("/year/{year}", response_model=List[Movie])
def get_movies_by_year(
    year: int,
    session: Session = Depends(get_session)
):
    statement = select(Movie).where(Movie.release_date >= f"{year}-01-01",
                                    Movie.release_date <= f"{year}-12-31")
    movies = session.exec(statement).all()
    return movies



@router.get("/stats/count")
def get_movies_count(session: Session = Depends(get_session)):
    count = session.exec(select(Movie)).all()
    return {"total_movies": len(count)}


@router.get("/{movie_id}/full-details")
def get_movie_with_details(movie_id: int, session: Session = Depends(get_session)):
    from sqlalchemy.orm import joinedload
    statement = (
        select(Movie)
        .where(Movie.id_movie == movie_id)
        .options(joinedload(Movie.actors), joinedload(Movie.genres))
    )
    movie = session.exec(statement).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie