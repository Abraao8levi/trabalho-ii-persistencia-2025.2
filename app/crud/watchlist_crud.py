import logging
from typing import List, Optional

from sqlmodel import Session, asc, desc, func, select

from ...models.models import Watchlist
from .exceptions import DuplicateEntryException, NotFoundException

logger = logging.getLogger(__name__)

class WatchlistCRUD:
    def __init__(self, session: Session):
        self.session = session

    def add_to_watchlist(self, watchlist_data: dict) -> Watchlist:
        """Add movie to user's watchlist"""
        try:
            # Check if movie is already in user's watchlist
            existing_entry = self.session.exec(
                select(Watchlist).where(
                    Watchlist.id_user == watchlist_data["id_user"],
                    Watchlist.id_movie == watchlist_data["id_movie"]
                )
            ).first()
            
            if existing_entry:
                raise DuplicateEntryException("Movie already in user's watchlist")

            watchlist = Watchlist(**watchlist_data)
            self.session.add(watchlist)
            self.session.commit()
            self.session.refresh(watchlist)
            return watchlist

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding to watchlist: {str(e)}")
            raise

    def get_watchlist_item(self, watchlist_id: int) -> Watchlist:
        """Get watchlist item by ID"""
        item = self.session.get(Watchlist, watchlist_id)
        if not item:
            raise NotFoundException(f"Watchlist item with ID {watchlist_id} not found")
        return item

    def get_user_watchlist(
        self, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100,
        search_notes: Optional[str] = None,
        sort_by: str = "id_watchlist",
        sort_order: str = "desc"
    ) -> List[Watchlist]:
        """Get user's watchlist with filtering"""
        query = select(Watchlist).where(Watchlist.id_user == user_id)
        
        if search_notes:
            query = query.where(Watchlist.notes.contains(search_notes))
        
        # Apply sorting
        sort_column = getattr(Watchlist, sort_by, Watchlist.id_watchlist)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        query = query.offset(skip).limit(limit)
        
        return self.session.exec(query).all()

    def update_watchlist_item(self, watchlist_id: int, update_data: dict) -> Watchlist:
        """Update watchlist item"""
        try:
            item = self.get_watchlist_item(watchlist_id)
            
            for key, value in update_data.items():
                setattr(item, key, value)
            
            self.session.commit()
            self.session.refresh(item)
            return item

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating watchlist item {watchlist_id}: {str(e)}")
            raise

    def remove_from_watchlist(self, watchlist_id: int) -> bool:
        """Remove item from watchlist"""
        try:
            item = self.get_watchlist_item(watchlist_id)
            self.session.delete(item)
            self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error removing watchlist item {watchlist_id}: {str(e)}")
            raise

    def is_movie_in_watchlist(self, user_id: int, movie_id: int) -> bool:
        """Check if movie is in user's watchlist"""
        item = self.session.exec(
            select(Watchlist).where(
                Watchlist.id_user == user_id,
                Watchlist.id_movie == movie_id
            )
        ).first()
        return item is not None

    # Complex queries
    def get_most_watchlisted_movies(self, limit: int = 10) -> List[dict]:
        """Get most watchlisted movies"""
        query = (
            select(
                Watchlist.id_movie,
                func.count(Watchlist.id_watchlist).label("watchlist_count")
            )
            .group_by(Watchlist.id_movie)
            .order_by(desc("watchlist_count"))
            .limit(limit)
        )
        
        return self.session.exec(query).all()

    def get_user_watchlist_stats(self, user_id: int) -> dict:
        """Get user's watchlist statistics"""
        total_count = self.session.exec(
            select(func.count(Watchlist.id_watchlist))
            .where(Watchlist.id_user == user_id)
        ).first()
        
        with_notes_count = self.session.exec(
            select(func.count(Watchlist.id_watchlist))
            .where(
                Watchlist.id_user == user_id,
                Watchlist.notes.is_not(None)
            )
        ).first()
        
        return {
            "user_id": user_id,
            "total_watchlist_items": total_count or 0,
            "items_with_notes": with_notes_count or 0,
            "items_without_notes": (total_count or 0) - (with_notes_count or 0)
        }

    def search_watchlist_by_notes(self, user_id: int, search_term: str) -> List[Watchlist]:
        """Search user's watchlist by notes content"""
        query = (
            select(Watchlist)
            .where(
                Watchlist.id_user == user_id,
                Watchlist.notes.contains(search_term)
            )
            .order_by(desc(Watchlist.id_watchlist))
        )
        return self.session.exec(query).all()
