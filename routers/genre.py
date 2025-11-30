from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.crud.genre_crud import GenreCRUD
from app.crud.exceptions import NotFoundException, DuplicateEntryException, ValidationException
from app.schemas_models.genres import GenreCreate, GenreRead, GenreUpdate
from app.schemas_models.movies import MovieRead


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


@router.post("/", response_model=GenreRead, status_code=status.HTTP_201_CREATED)
def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        return crud.create_genre(genre.model_dump())
    except DuplicateEntryException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[GenreRead])
def read_genres(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        return crud.get_genres(offset, limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{genre_id}", response_model=GenreRead)
def read_genre(genre_id: int, session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        return crud.get_genre_by_id(genre_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{genre_id}", response_model=GenreRead)
def update_genre(genre_id: int, genre: GenreUpdate, session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        return crud.update_genre(genre_id, genre.model_dump(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{genre_id}")
def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        crud.delete_genre(genre_id)
        return {"message": "Genre deleted successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{genre_id}/movies/", response_model=List[MovieRead])
def read_movies_of_genre(genre_id: int, session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        return crud.get_genre_movies(genre_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{genre_id}/movies/{movie_id}", response_model=MovieRead)
def add_movie_to_genre(genre_id: int, movie_id: int, session: Session = Depends(get_session)):
    try:
        crud = GenreCRUD(session)
        return crud.add_movie_to_genre(genre_id, movie_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateEntryException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
