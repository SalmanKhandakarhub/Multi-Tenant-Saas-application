from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, password):
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*]', password):
            raise ValueError("Password must contain at least one special character")
        return password

class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    password: str | None = None
    
class UserInDBBase(UserBase):
    id: int
    tenant_id: int
    
    class Config:
        orm_mode = True
        
class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
    
    