from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from typing import List, Optional
from app.database import get_session
from models.models import User
from sqlalchemy.orm import joinedload

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User, session: Session = Depends(get_session)):
    
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    

    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=List[User])
def get_users(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session)
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: User, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
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