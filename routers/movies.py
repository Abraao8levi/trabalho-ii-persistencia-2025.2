# app/routers/movies.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.crud.crud_movies import (
    create_movie,
    delete_movie,
    get_movie,
    get_movies,
    update_movie,
)
from app.database import get_session
from app.schemas import MovieCreate, MovieRead, MovieUpdate
from models.models import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.post("/", response_model=MovieRead)
def create_movie_endpoint(movie: MovieCreate, session: Session = Depends(get_session)):
    return create_movie(session, movie)



@router.get("/", response_model=List[MovieRead])
def get_movies_endpoint(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
):
    return get_movies(session, offset, limit)




@router.get("/{movie_id}", response_model=MovieRead)
def get_movie_endpoint(movie_id: int, session: Session = Depends(get_session)):
    movie = get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie



@router.put("/{movie_id}", response_model=MovieRead)
def update_movie_endpoint(movie_id: int, movie_update: MovieUpdate, session: Session = Depends(get_session)):
    movie = update_movie(session, movie_id, movie_update)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie



@router.delete("/{movie_id}")
def delete_movie_endpoint(movie_id: int, session: Session = Depends(get_session)):
    movie = delete_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
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