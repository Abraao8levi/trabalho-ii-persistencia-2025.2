from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from typing import List
import logging
from models.models import Genre, Movie, MovieGenre
from app.crud.exceptions import NotFoundException, DuplicateEntryException, ValidationException

logger = logging.getLogger(__name__)

class GenreCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_genre(self, data: dict) -> Genre:
        existing = self.session.exec(
            select(Genre).where(Genre.name == data.get("name"))
        ).first()

        if existing:
            raise DuplicateEntryException("Genre already exists")

        try:
            genre = Genre.model_validate(data)
            self.session.add(genre)
            self.session.commit()
            self.session.refresh(genre)
            return genre
        except Exception:
            raise ValidationException("Error creating genre")

    def get_genres(self, offset: int = 0, limit: int = 10) -> List[Genre]:
        statement = (
            select(Genre)
            .offset(offset)
            .limit(limit)
            .options(joinedload(Genre.movies))
        )
        return self.session.exec(statement).unique().all()

    def get_genre_by_id(self, genre_id: int) -> Genre:
        statement = (
            select(Genre)
            .where(Genre.id_genre == genre_id)
            .options(joinedload(Genre.movies))
        )
        genre = self.session.exec(statement).first()

        if not genre:
            raise NotFoundException("Genre not found")

        return genre

    def update_genre(self, genre_id: int, data: dict) -> Genre:
        genre = self.session.get(Genre, genre_id)

        if not genre:
            raise NotFoundException("Genre not found")

        for key, value in data.items():
            setattr(genre, key, value)

        self.session.add(genre)
        self.session.commit()
        self.session.refresh(genre)

        return genre

    def delete_genre(self, genre_id: int):
        genre = self.session.get(Genre, genre_id)

        if not genre:
            raise NotFoundException("Genre not found")

        self.session.delete(genre)
        self.session.commit()

    def get_genre_movies(self, genre_id: int) -> List[Movie]:
        genre = self.session.get(Genre, genre_id)
        if not genre:
            raise NotFoundException("Genre not found")

        statement = (
            select(Movie)
            .join(MovieGenre)
            .where(MovieGenre.genre_id == genre_id)
        )

        return self.session.exec(statement).all()

    def add_movie_to_genre(self, genre_id: int, movie_id: int):
        genre = self.session.get(Genre, genre_id)
        movie = self.session.get(Movie, movie_id)

        if not genre:
            raise NotFoundException("Genre not found")

        if not movie:
            raise NotFoundException("Movie not found")

        existing_link = self.session.exec(
            select(MovieGenre).where(
                MovieGenre.genre_id == genre_id,
                MovieGenre.movie_id == movie_id
            )
        ).first()

        if existing_link:
            raise DuplicateEntryException("This movie is already associated with this genre")

        # Cria o vínculo
        link = MovieGenre(genre_id=genre_id, movie_id=movie_id)
        self.session.add(link)
        self.session.commit()

        return movie