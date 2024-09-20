from sqlalchemy.orm import Session
from app.models.user import User
from app.crud.crud_user import users_crud
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        return users_crud.get(db, id=user_id)
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return users_crud.get_by_email(db, email=email)
    
    @staticmethod
    def create_user(db: Session, user_in: UserCreate, tenant_id: int) -> User:
        return users_crud.create(db, obj_in=user_in, tenant_id=tenant_id)

    @staticmethod
    def update_user(db: Session, db_obj: User, user_in: UserUpdate) -> User:
        return users_crud.update(db, db_obj=db_obj, obj_in=user_in)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        return users_crud.authenticate(db, email=email, password=password)

user_service = UserService()