from typing import List, Optional

from sqlmodel import Session, select

from models.models import User
from app.schemas_models.users import UserCreate, UserUpdate

def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Retorna um usuário pelo seu ID.
    """
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retorna um usuário pelo seu email.
    """
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retorna uma lista de usuários com paginação.
    """
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados.
    """
    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    Atualiza as informações de um usuário existente.
    """
    db_user = db.get(User, user_id)
    if not db_user:
        return None
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    """
    Deleta um usuário do banco de dados.
    """
    db_user = db.get(User, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user