# app/routers/movies.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.crud.crud_movies import (create_movie, delete_movie, get_movie,
                                  get_movies, update_movie)
from app.crud.exceptions import ValidationException
from app.database import get_session
from app.schemas_models.movies import MovieCreate, MovieRead, MovieUpdate
from app.schemas_models.aggregations import MovieFullInfo
from models.models import Movie
from app.crud.crud_movies import get_movie_full_info
from app.crud.exceptions import NotFoundException

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.post("/", response_model=MovieRead)
def create_movie_endpoint(movie: MovieCreate, session: Session = Depends(get_session)):
    """Create a new movie"""
    return create_movie(session, movie)



@router.get("/", response_model=List[MovieRead])
def get_movies_endpoint(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
):
    """Get a list of movies"""
    try:
        return get_movies(session, offset, limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")




@router.get("/{movie_id}", response_model=MovieRead)
def get_movie_endpoint(movie_id: int, session: Session = Depends(get_session)):
    """Get movie by ID"""
    movie = get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie



@router.put("/{movie_id}", response_model=MovieRead)
def update_movie_endpoint(movie_id: int, movie_update: MovieUpdate, session: Session = Depends(get_session)):
    """Update a movie"""
    try:
        movie = update_movie(session, movie_id, movie_update)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except HTTPException:
        raise
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")



@router.delete("/{movie_id}")
def delete_movie_endpoint(movie_id: int, session: Session = Depends(get_session)):
    """Delete a movie"""
    try:
        movie = delete_movie(session, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return {"message": "Movie deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search/{title}", response_model=List[Movie])
def search_movies_by_title(
    title: str,
    session: Session = Depends(get_session)
):
    """Search movies by title"""
    try:
        statement = select(Movie).where(Movie.title.ilike(f"%{title}%"))
        movies = session.exec(statement).all()
        return movies
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")



@router.get("/year/{year}", response_model=List[Movie])
def get_movies_by_year(
    year: int,
    session: Session = Depends(get_session)
):
    """Get movies by release year"""
    try:
        statement = select(Movie).where(Movie.release_date >= f"{year}-01-01",
                                        Movie.release_date <= f"{year}-12-31")
        movies = session.exec(statement).all()
        return movies
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")



@router.get("/stats/count")
def get_movies_count(session: Session = Depends(get_session)):
    """Get total count of movies"""
    try:
        count = session.exec(select(Movie)).all()
        return {"total_movies": len(count)}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{movie_id}/stats")
def get_movie_stats(movie_id: int, session: Session = Depends(get_session)):
    """Get movie statistics including actor count"""
    try:
        from sqlalchemy.orm import joinedload
        statement = (
            select(Movie)
            .where(Movie.id_movie == movie_id)
            .options(joinedload(Movie.actors))
        )
        movie = session.exec(statement).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        actor_count = len(movie.actors) if movie.actors else 0
        return {"movie_id": movie_id, "actor_count": actor_count}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{movie_id}/actors/", response_model=List[ActorRead])
def get_movie_actors(movie_id: int, session: Session = Depends(get_session)):
    """Get actors of a movie"""
    try:
        from sqlalchemy.orm import joinedload
        statement = (
            select(Movie)
            .where(Movie.id_movie == movie_id)
            .options(joinedload(Movie.actors))
        )
        movie = session.exec(statement).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie.actors if movie.actors else []
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{movie_id}/full-details", response_model=MovieFullInfo)
def get_movie_with_details(movie_id: int, session: Session = Depends(get_session)):
    try:
        return get_movie_full_info(session, movie_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error")