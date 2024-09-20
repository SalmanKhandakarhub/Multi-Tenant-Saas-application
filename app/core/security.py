from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta
from app.core.config import Settings
import jose 

pwc_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_tocken(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp" : expires,
        "sub" : str(subject)
    }
    encode_jwt = jose.jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encode_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwc_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwc_context.hash(password)