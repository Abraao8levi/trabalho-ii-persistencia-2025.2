from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.database import get_session
from models.models import Actor, Movie, MovieActor
from typing import List
from app.schemas import ActorCreate, ActorRead, ActorUpdate

router = APIRouter(
    prefix="/actors",
    tags=["Actors"]
)

@router.post("/", response_model=ActorCreate)
def create_actor(actor: ActorCreate, session: Session = Depends(get_session)):
    db_actor = Actor.model_validate(actor)
    session.add(db_actor)
    session.commit()
    session.refresh(db_actor)
    return db_actor

@router.get("/", response_model=List[Actor])
def get_actors(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    statement = (
        select(Actor).offset(offset).limit(limit).options(joinedload(Actor.movies))
    )
    return session.exec(statement).unique().all()

@router.get("/{actor_id}", response_model=ActorRead)
def get_actor_by_id(actor_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Actor).where(Actor.id_actor == actor_id).options(joinedload(Actor.movies))
    )
    actor = session.exec(statement).first()

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor


@router.put("/{actor_id}", response_model=ActorUpdate)
def update_actor(actor_id: int, actor: Actor, session: Session = Depends(get_session)):
    actorToUpdate = session.get(Actor, actor_id)

    if not actorToUpdate:
        raise HTTPException(status_code=404, detail="Actor not found")
    for key, value in actor.model_dump(exclude_unset=True).items():
        setattr(actorToUpdate, key, value)
    
    session.add(actorToUpdate)
    session.commit()
    session.refresh(actorToUpdate)
    return actorToUpdate


@router.delete("/{actor_id}")
def delete_actor(actor_id: int, session: Session = Depends(get_session)):
    actor = session.get(Actor, actor_id)

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    session.delete(actor)
    session.commit()

    return {"ok": True}


@router.post("/{actor_id}/movies/{movie_id}", response_model=Movie)
def add_movie_to_actor(actor_id: int, movie_id: int, session: Session = Depends(get_session)):
    actor = session.get(Actor, actor_id)
    movie = session.get(Movie, movie_id)

    if not actor or not movie:
        raise HTTPException(status_code=404, detail="Actor or Movie not found")

    link = session.exec(
        select(MovieActor).where(
            MovieActor.actor_id == actor_id,
            MovieActor.movie_id == movie_id
        )
    ).first()

    if link:
        return movie  

    new_link = MovieActor(actor_id=actor_id, movie_id=movie_id)
    session.add(new_link)
    session.commit()

    return movie

@router.get("/{actor_id}/movies/", response_model=List[Movie])
def read_movies_of_actor(actor_id: int, session: Session = Depends(get_session)):

    statement = (
        select(Movie)
        .join(MovieActor)
        .where(MovieActor.actor_id == actor_id)
    )
    return session.exec(statement).all()


@router.delete("/{actor_id}/movies/{movie_id}")
def remove_movie_from_actor(actor_id: int, movie_id: int, session: Session = Depends(get_session)):

    link = session.exec(
        select(MovieActor).where(
            MovieActor.actor_id == actor_id,
            MovieActor.movie_id == movie_id
        )
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link actor-movie not found")

    session.delete(link)
    session.commit()

    return {"ok": True}