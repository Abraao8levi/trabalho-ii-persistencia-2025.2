from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.crud.exceptions import (
    DuplicateEntryException,
    NotFoundException,
    ValidationException,
)
from app.crud.review_crud import ReviewCRUD
from app.database import get_session
from app.schemas_models.reviews import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    """Create a new review"""
    try:
        crud = ReviewCRUD(session)
        return crud.create_review(review.dict())
    except DuplicateEntryException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, session: Session = Depends(get_session)):
    """Get review by ID"""
    try:
        crud = ReviewCRUD(session)
        return crud.get_review_by_id(review_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[ReviewRead])
def get_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    movie_id: Optional[int] = None,
    user_id: Optional[int] = None,
    min_rating: Optional[float] = Query(None, ge=0.5, le=5.0),
    max_rating: Optional[float] = Query(None, ge=0.5, le=5.0),
    search_content: Optional[str] = None,
    sort_by: str = Query("id_review", regex="^(id_review|rating|movie_id|user_id)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    session: Session = Depends(get_session)
):
    """Get reviews with filtering and sorting"""
    try:
        crud = ReviewCRUD(session)
        return crud.get_reviews(
            skip=skip,
            limit=limit,
            movie_id=movie_id,
            user_id=user_id,
            min_rating=min_rating,
            max_rating=max_rating,
            search_content=search_content,
            sort_by=sort_by,
            sort_order=sort_order
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, review: ReviewUpdate, session: Session = Depends(get_session)):
    """Update a review"""
    try:
        crud = ReviewCRUD(session)
        return crud.update_review(review_id, review.dict(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{review_id}")
def delete_review(review_id: int, session: Session = Depends(get_session)):
    """Delete a review"""
    try:
        crud = ReviewCRUD(session)
        crud.delete_review(review_id)
        return {"message": "Review deleted successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

# Complex queries endpoints
@router.get("/movie/{movie_id}/stats")
def get_movie_review_stats(movie_id: int, session: Session = Depends(get_session)):
    """Get review statistics for a movie"""
    try:
        crud = ReviewCRUD(session)
        return crud.get_movie_review_stats(movie_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}/history")
def get_user_review_history(user_id: int, session: Session = Depends(get_session)):
    """Get user's review history"""
    try:
        crud = ReviewCRUD(session)
        return crud.get_user_review_history(user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/movies/top-rated")
def get_top_rated_movies(
    limit: int = Query(10, ge=1, le=50),
    session: Session = Depends(get_session)
):
    """Get top rated movies"""
    try:
        crud = ReviewCRUD(session)
        return crud.get_top_rated_movies(limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/content")
def search_reviews_by_content(
    q: str = Query(..., min_length=1, description="Search term"),
    session: Session = Depends(get_session)
):
    """Search reviews by content"""
    try:
        crud = ReviewCRUD(session)
        return crud.search_reviews_by_content(q)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
