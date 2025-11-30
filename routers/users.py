from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from app.crud.crud_users import (
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_users,
    update_user,
)
from app.database import get_session
from app.schemas_models.users import UserCreate, UserRead, UserUpdate
from models.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_data: UserCreate, session: Session = Depends(get_session)):

    existing_user = get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Check for existing username - since there's no get_user_by_username, I'll keep this direct query
    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    return create_user(session, user_data)


@router.get("/", response_model=List[UserRead])
def get_users_endpoint(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
):
    return get_users(session, offset, limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = update_user(session, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    user = delete_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}




@router.get("/search/{username}", response_model=List[User])
def search_users_by_username(
    username: str,
    session: Session = Depends(get_session)
):
    statement = select(User).where(User.username.ilike(f"%{username}%"))
    users = session.exec(statement).all()
    return users


@router.get("/stats/count")
def get_users_count(session: Session = Depends(get_session)):
    count = session.exec(select(User)).all()
    return {"total_users": len(count)}


@router.get("/created/{start_date}/{end_date}", response_model=List[User])
def get_users_by_creation_date(
    start_date: str,
    end_date: str,
    session: Session = Depends(get_session)
):
    statement = select(User).where(
        User.created_at >= start_date,
        User.created_at <= end_date
    )
    users = session.exec(statement).all()
    return users


@router.get("/{user_id}/reviews")
def get_user_with_reviews(user_id: int, session: Session = Depends(get_session)):
    statement = (
        select(User)
        .where(User.id_user == user_id)
        .options(joinedload(User.reviews))
    )
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user