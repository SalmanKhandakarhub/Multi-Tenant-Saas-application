from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum as Pyenum
from typing import Optional
from datetime import datetime


class UserStatusEnum(str, Pyenum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class UpdateStatus(BaseModel):
    id: int
    status: UserStatusEnum    
    
    
class StatusUpdateResponse(BaseModel):
    id: int
    email: EmailStr
    status: Optional[UserStatusEnum] = UserStatusEnum.ACTIVE
    is_super_admin: Optional[bool] = False
    
    class Config:
        orm_mode = True
        from_attributes = True 
    
    
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    contact_no: Optional[str] = None
 

class GetUserId(BaseModel):
    id: int


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_no: Optional[str] = None
    image: Optional[str] = None

        
class UserResponse(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    contact_no: Optional[str] = None
    status: Optional[UserStatusEnum] = UserStatusEnum.ACTIVE
    is_super_admin: Optional[bool] = False
    image: Optional[str] = None  
    
    class Config:
        orm_mode = True
        from_attributes = True 
        
        
class AllUserResponse(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    contact_no: Optional[str] = None
    image: Optional[str] = None 
    status: Optional[UserStatusEnum] = UserStatusEnum.ACTIVE
    is_super_admin: Optional[bool] = False

    class Config:
        orm_mode = True
        from_attributes = True 


class LoginResponse(BaseModel):
    message: str
    access_token: str
    user: UserResponse

    class Config:
        orm_mode = True

        
class ForgetPasswordCreate(BaseModel):
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")    
    confirm_password: str
    
    @validator('confirm_password')
    def password_match(cls, confirm_password, values):
        password = values.get('password')
        if password != confirm_password:
            raise ValueError("Password do not metch")
        return confirm_password
    
    
class ChangePasswordCreate(BaseModel):
    old_password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")    
    confirm_password: str
    
    @validator('confirm_password')
    def password_match(cls, confirm_password, values):
        password = values.get('password')
        if password != confirm_password:
            raise ValueError("Password do not metch")
        return confirm_password


class GetCredential(BaseModel):
    email: Optional[EmailStr] = None  
    
    
class AddUser(BaseModel):
    first_name_en: str
    last_name_en: str
    email: EmailStr
    organization_name: str
    commercial_id: str
    
    
class AddUserResponse(BaseModel):
    id: int
    name: Optional[str]
    email: EmailStr
    contact_no: Optional[str] = None
    status: Optional[UserStatusEnum] = UserStatusEnum.ACTIVE
    created_at: Optional[datetime]  

    class Config:
        orm_mode = True
        from_attributes = True
        
        
        