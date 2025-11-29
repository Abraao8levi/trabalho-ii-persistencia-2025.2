import logging
from typing import List, Optional

from sqlmodel import Session, asc, desc, func, select

from models.models import Review
from .exceptions import (DuplicateEntryException, NotFoundException,
                         ValidationException)

logger = logging.getLogger(__name__)

class ReviewCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_review(self, review_data: dict) -> Review:
        """Create a new review"""
        try:
            # Check if review already exists for this user and movie
            existing_review = self.session.exec(
                select(Review).where(
                    Review.user_id == review_data["user_id"],
                    Review.movie_id == review_data["movie_id"]
                )
            ).first()
            
            if existing_review:
                raise DuplicateEntryException("User already reviewed this movie")

            # Validate rating
            if not (0.5 <= review_data["rating"] <= 5.0):
                raise ValidationException("Rating must be between 0.5 and 5.0")

            review = Review(**review_data)
            self.session.add(review)
            self.session.commit()
            self.session.refresh(review)
            return review

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating review: {str(e)}")
            raise

    def get_review_by_id(self, review_id: int) -> Review:
        """Get review by ID"""
        review = self.session.get(Review, review_id)
        if not review:
            raise NotFoundException(f"Review with ID {review_id} not found")
        return review

    def get_reviews(
        self, 
        skip: int = 0, 
        limit: int = 100,
        movie_id: Optional[int] = None,
        user_id: Optional[int] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        search_content: Optional[str] = None,
        sort_by: str = "id_review",
        sort_order: str = "asc"
    ) -> List[Review]:
        """Get reviews with filtering and sorting"""
        query = select(Review)
        
        # Apply filters
        if movie_id:
            query = query.where(Review.movie_id == movie_id)
        if user_id:
            query = query.where(Review.user_id == user_id)
        if min_rating is not None:
            query = query.where(Review.rating >= min_rating)
        if max_rating is not None:
            query = query.where(Review.rating <= max_rating)
        if search_content:
            query = query.where(Review.content.contains(search_content))
        
        # Apply sorting
        sort_column = getattr(Review, sort_by, Review.id_review)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        return self.session.exec(query).all()

    def update_review(self, review_id: int, review_data: dict) -> Review:
        """Update a review"""
        try:
            review = self.get_review_by_id(review_id)
            
            # Validate rating if provided
            if "rating" in review_data and not (0.5 <= review_data["rating"] <= 5.0):
                raise ValidationException("Rating must be between 0.5 and 5.0")
            
            for key, value in review_data.items():
                setattr(review, key, value)
            
            self.session.commit()
            self.session.refresh(review)
            return review

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating review {review_id}: {str(e)}")
            raise

    def delete_review(self, review_id: int) -> bool:
        """Delete a review"""
        try:
            review = self.get_review_by_id(review_id)
            self.session.delete(review)
            self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting review {review_id}: {str(e)}")
            raise

    # Complex queries
    def get_movie_review_stats(self, movie_id: int) -> dict:
        """Get review statistics for a movie"""
        stats = self.session.exec(
            select(
                func.count(Review.id_review).label("total_reviews"),
                func.avg(Review.rating).label("average_rating"),
                func.min(Review.rating).label("min_rating"),
                func.max(Review.rating).label("max_rating")
            ).where(Review.movie_id == movie_id)
        ).first()
        
        return {
            "movie_id": movie_id,
            "total_reviews": stats[0] or 0,
            "average_rating": round(float(stats[1] or 0), 2),
            "min_rating": stats[2] or 0,
            "max_rating": stats[3] or 0
        }

    def get_user_review_history(self, user_id: int) -> List[Review]:
        """Get user's review history with movie details"""
        query = (
            select(Review)
            .where(Review.user_id == user_id)
            .order_by(desc(Review.id_review))
        )
        return self.session.exec(query).all()

    def get_top_rated_movies(self, limit: int = 10) -> List[dict]:
        """Get top rated movies based on reviews"""
        query = (
            select(
                Review.movie_id,
                func.avg(Review.rating).label("avg_rating"),
                func.count(Review.id_review).label("review_count")
            )
            .group_by(Review.movie_id)
            .having(func.count(Review.id_review) >= 3)  # Minimum reviews
            .order_by(desc("avg_rating"))
            .limit(limit)
        )
        
        return self.session.exec(query).all()

    def search_reviews_by_content(self, search_term: str) -> List[Review]:
        """Search reviews by content text"""
        query = (
            select(Review)
            .where(Review.content.contains(search_term))
            .order_by(desc(Review.id_review))
        )
        return self.session.exec(query).all()
