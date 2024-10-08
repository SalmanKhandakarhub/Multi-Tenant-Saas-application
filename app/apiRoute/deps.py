from typing import Generator
from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.models.user import User
from jose import JWTError, jwt   
from app.core.config import settings
from pydantic import ValidationError
from app import crud, models, schemas
from app.core import security

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/apiRoute/v1/login/access-token")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.users_crud.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not crud.users_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
