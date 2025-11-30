from typing import List, Optional

from sqlmodel import Session, select

from ... import models, schemas


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Retorna um usuário pelo seu ID.
    """
    return db.get(models.User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Retorna um usuário pelo seu email.
    """
    statement = select(models.User).where(models.User.email == email)
    return db.exec(statement).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    Retorna uma lista de usuários com paginação.
    """
    statement = select(models.User).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Cria um novo usuário no banco de dados.
    """
    db_user = models.User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """
    Atualiza as informações de um usuário existente.
    """
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    Deleta um usuário do banco de dados.
    """
    db_user = db.get(models.User, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user