from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.crud.actor_crud import ActorCRUD
from app.crud.exceptions import (DuplicateEntryException, NotFoundException,
                                 ValidationException)
from app.database import get_session
from app.schemas_models.actors import ActorCreate, ActorRead, ActorUpdate
from app.schemas_models.movies import MovieRead

router = APIRouter(
    prefix="/actors",
    tags=["Actors"]
)

@router.post("/", response_model=ActorRead, status_code=status.HTTP_201_CREATED)
def create_actor(actor: ActorCreate, session: Session = Depends(get_session)):
    """Create a new actor"""
    try:
        crud = ActorCRUD(session)
        return crud.create_actor(actor.model_dump())
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateEntryException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[ActorRead])
def get_actors(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """Get a list of actors"""
    try:
        crud = ActorCRUD(session)
        return crud.get_actors(offset, limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{actor_id}", response_model=ActorRead)
def get_actor_by_id(actor_id: int, session: Session = Depends(get_session)):
    """Get actor by ID"""
    try:
        crud = ActorCRUD(session)
        return crud.get_actor_by_id(actor_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{actor_id}", response_model=ActorRead)
def update_actor(actor_id: int, actor: ActorUpdate, session: Session = Depends(get_session)):
    """Update an actor"""
    try:
        crud = ActorCRUD(session)
        return crud.update_actor(actor_id, actor.model_dump(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{actor_id}")
def delete_actor(actor_id: int, session: Session = Depends(get_session)):
    """Delete an actor"""
    try:
        crud = ActorCRUD(session)
        crud.delete_actor(actor_id)
        return {"message": "Actor deleted successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{actor_id}/movies/{movie_id}", response_model=MovieRead)
def add_movie_to_actor(actor_id: int, movie_id: int, session: Session = Depends(get_session)):
    """Add movie to actor"""
    try:
        crud = ActorCRUD(session)
        return crud.add_movie_to_actor(actor_id, movie_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{actor_id}/movies/", response_model=List[MovieRead])
def get_movies_of_actor(actor_id: int, session: Session = Depends(get_session)):
    """Get movies of an actor"""
    try:
        crud = ActorCRUD(session)
        return crud.get_actor_movies(actor_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{actor_id}/movies/{movie_id}")
def remove_movie_from_actor(actor_id: int, movie_id: int, session: Session = Depends(get_session)):
    """Remove movie from actor"""
    try:
        crud = ActorCRUD(session)
        return crud.remove_movie_from_actor(actor_id, movie_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

# @router.get("/search/{name}", response_model=List[ActorRead])
# def search_actors_by_name(name: str, session: Session = Depends(get_session)):
#     """Search actors by name"""
#     try:
#         crud = ActorCRUD(session)
#         return crud.search_actors_by_name(name)
#     except Exception:
#         raise HTTPException(status_code=500, detail="Internal server error")
