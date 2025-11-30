from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import List, Optional
from app.database import get_session
from app.crud.watchlist_crud import WatchlistCRUD
from app.crud.exceptions import NotFoundException, DuplicateEntryException
from app.schemas_models.watchlist import WatchlistCreate, WatchlistUpdate, WatchlistRead

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.post("/", response_model=WatchlistRead, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(watchlist: WatchlistCreate, session: Session = Depends(get_session)):
    """Add movie to user's watchlist"""
    try:
        crud = WatchlistCRUD(session)
        return crud.add_to_watchlist(watchlist.model_dump())
    except DuplicateEntryException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{watchlist_id}", response_model=WatchlistRead)
def get_watchlist_item(watchlist_id: int, session: Session = Depends(get_session)):
    """Get watchlist item by ID"""
    try:
        crud = WatchlistCRUD(session)
        return crud.get_watchlist_item(watchlist_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}", response_model=List[WatchlistRead])
def get_user_watchlist(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search_notes: Optional[str] = None,
    sort_by: str = Query("id_watchlist", regex="^(id_watchlist|id_movie)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    session: Session = Depends(get_session)
):
    """Get user's watchlist"""
    try:
        crud = WatchlistCRUD(session)
        return crud.get_user_watchlist(
            user_id=user_id,
            skip=skip,
            limit=limit,
            search_notes=search_notes,
            sort_by=sort_by,
            sort_order=sort_order
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{watchlist_id}", response_model=WatchlistRead)
def update_watchlist_item(
    watchlist_id: int, 
    watchlist: WatchlistUpdate, 
    session: Session = Depends(get_session)
):
    """Update watchlist item"""
    try:
        crud = WatchlistCRUD(session)
        return crud.update_watchlist_item(watchlist_id, watchlist.model_dump(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{watchlist_id}")
def remove_from_watchlist(watchlist_id: int, session: Session = Depends(get_session)):
    """Remove item from watchlist"""
    try:
        crud = WatchlistCRUD(session)
        crud.remove_from_watchlist(watchlist_id)
        return {"message": "Item removed from watchlist successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Complex queries endpoints
@router.get("/check/{user_id}/{movie_id}")
def check_movie_in_watchlist(user_id: int, movie_id: int, session: Session = Depends(get_session)):
    """Check if movie is in user's watchlist"""
    try:
        crud = WatchlistCRUD(session)
        return {"in_watchlist": crud.is_movie_in_watchlist(user_id, movie_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/movies/most-watchlisted")
def get_most_watchlisted_movies(
    limit: int = Query(10, ge=1, le=50),
    session: Session = Depends(get_session)
):
    """Get most watchlisted movies"""
    try:
        crud = WatchlistCRUD(session)
        return crud.get_most_watchlisted_movies(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}/stats")
def get_user_watchlist_stats(user_id: int, session: Session = Depends(get_session)):
    """Get user's watchlist statistics"""
    try:
        crud = WatchlistCRUD(session)
        return crud.get_user_watchlist_stats(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}/search/notes")
def search_watchlist_by_notes(
    user_id: int,
    q: str = Query(..., min_length=1, description="Search term"),
    session: Session = Depends(get_session)
):
    """Search user's watchlist by notes"""
    try:
        crud = WatchlistCRUD(session)
        return crud.search_watchlist_by_notes(user_id, q)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")