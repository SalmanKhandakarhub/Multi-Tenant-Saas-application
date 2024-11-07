from passlib.context import CryptContext # type: ignore
from datetime import datetime, timedelta
from jose import JWTError, jwt   # type: ignore
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from random import choice
import string

from core.config import settings
from core.database_manager import get_master_db
from models.master_models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/master/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_tocken(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


def generate_reset_token(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1) 
    token_data ={
        "sub" : user_id,
        "exp" : expiration
    }
    encode_jwt = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
    
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_master_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = verify_access_token(token, credentials_exception)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


def generate_random_password(length: int = 12) -> str:
    character = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(choice(character) for _ in range(length))
    return random_password
    