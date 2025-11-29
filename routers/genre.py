from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.database import get_session
from models.models import Genre, Movie, MovieGenre
from typing import List

router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

@router.post("/", response_model=Genre)
def create_genre(genre: Genre, session: Session = Depends(get_session)):
    genderExistingVerification = session.exec(select(Genre).where(Genre.name == genre.name)).first()
    if genderExistingVerification:
        raise HTTPException(status_code=400, detail="Genre already exists")
    
    session.add(genre)
    session.commit()
    session.refresh(genre)
    return genre

@router.get("/", response_model=List[Genre])
def read_genres(offset: int = 0, 
                limit: int = Query(default=10, le=100),
                session: Session = Depends(get_session)):

    statement = (
        select(Genre)
        .offset(offset)
        .limit(limit)
        .options(joinedload(Genre.movies))
    )

    return session.exec(statement).unique().all()

@router.get("/{genre_id}", response_model=Genre)
def read_genre(genre_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Genre)
        .where(Genre.id_genre == genre_id)
        .options(joinedload(Genre.movies))
    )
    genre = session.exec(statement).first()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre

@router.put("/{genre_id}", response_model=Genre)
def update_genre(genre_id: int, genre: Genre, session: Session = Depends(get_session)):
    db_genre = session.get(Genre, genre_id)

    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    for key, value in genre.model_dump(exclude_unset=True).items():
        setattr(db_genre, key, value)

    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre

@router.delete("/{genre_id}")
def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    genre = session.get(Genre, genre_id)

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    session.delete(genre)
    session.commit()

    return {"ok": True}

@router.get("/{genre_id}/movies/", response_model=List[Movie])
def read_movies_of_genre(genre_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Movie)
        .join(MovieGenre)
        .where(MovieGenre.genre_id == genre_id)
    )

    return session.exec(statement).all()