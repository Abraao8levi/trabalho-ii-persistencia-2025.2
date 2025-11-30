import logging
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.crud.exceptions import NotFoundException, DuplicateEntryException, ValidationException
from models.models import Actor, Movie, MovieActor
from app.schemas_models.actors import ActorCreate, ActorUpdate
from typing import List

logger = logging.getLogger(__name__)

class ActorCRUD:
    def __init__(self, session: Session):
        self.session = session
    
    def create_actor(self, data: dict) -> Actor:
        try:
            actor = Actor.model_validate(data)
            self.session.add(actor)
            self.session.commit()
            self.session.refresh(actor)
            return actor
        except Exception:
            raise ValidationException("Error creating actor")
        
    def get_actors(self, offset: int = 0, limit: int = 10) -> List[Actor]:
        statement = (
            select(Actor)
            .offset(offset)
            .limit(limit)
            .options(joinedload(Actor.movies))
        )
        return self.session.exec(statement).unique().all()
    
    def get_actor_by_id(self, actor_id: int) -> Actor:
        statement = (
            select(Actor)
            .where(Actor.id_actor == actor_id)
            .options(joinedload(Actor.movies))
        )
        actor = self.session.exec(statement).first()

        if not actor:
            raise NotFoundException("Actor not found")

        return actor
    
    def update_actor(self, actor_id: int, data: dict) -> Actor:
        actor = self.session.get(Actor, actor_id)

        if not actor:
            raise NotFoundException("Actor not found")

        for key, value in data.items():
            setattr(actor, key, value)

        self.session.add(actor)
        self.session.commit()
        self.session.refresh(actor)
        return actor
    
    def delete_actor(self, actor_id: int):
        actor = self.session.get(Actor, actor_id)

        if not actor:
            raise NotFoundException("Actor not found")

        self.session.delete(actor)
        self.session.commit()
    
    def add_movie_to_actor(self, actor_id: int, movie_id: int) -> Movie:
        actor = self.session.get(Actor, actor_id)
        movie = self.session.get(Movie, movie_id)

        if not actor or not movie:
            raise NotFoundException("Actor or Movie not found")

        link = self.session.exec(
            select(MovieActor).where(
                MovieActor.actor_id == actor_id,
                MovieActor.movie_id == movie_id
            )
        ).first()

        if link:
            return movie  # already linked

        new_link = MovieActor(actor_id=actor_id, movie_id=movie_id)
        self.session.add(new_link)
        self.session.commit()

        return movie
    
    def get_actor_movies(self, actor_id: int) -> List[Movie]:
        actor = self.session.get(Actor, actor_id)
        if not actor:
            raise NotFoundException("Actor not found")

        statement = (
            select(Movie)
            .join(MovieActor)
            .where(MovieActor.actor_id == actor_id)
        )
        return self.session.exec(statement).all()
    
    def remove_movie_from_actor(self, actor_id: int, movie_id: int):
        link = self.session.exec(
            select(MovieActor).where(
                MovieActor.actor_id == actor_id,
                MovieActor.movie_id == movie_id
            )
        ).first()

        if not link:
            raise NotFoundException("Link actor-movie not found")

        self.session.delete(link)
        self.session.commit()

        return {"ok": True}