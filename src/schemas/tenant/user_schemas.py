from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum as Pyenum
from typing import Optional
from datetime import datetime


class UserRoleEnum(str,Pyenum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"


class UpdateRole(BaseModel):
    id: int
    role: UserRoleEnum
    
    
class UpdateRoleResponse(BaseModel):
    id: int
    email: EmailStr
    role:  Optional[UserRoleEnum]= UserRoleEnum.ADMIN
    
    class Config:
        orm_mode = True
        from_attributes = True  
        
    
class UserCreate(BaseModel):
    first_name_en: str
    second_name_en: str
    last_name_en: str
    first_name_ar: Optional[str] = None
    second_name_ar: Optional[str] = None
    last_name_ar: Optional[str] = None
    user_name: str
    profession: Optional[str] = None
    position: Optional[str] = None
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    email: EmailStr
    contact_no: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    image: Optional[str] = None
    upload_cv: Optional[str] = None
    
    
class GetUserId(BaseModel):
    id: int
    
    
class UserUpdate(BaseModel):
    id: int
    first_name_en: str
    second_name_en: str
    last_name_en: str
    first_name_ar: Optional[str] = None
    second_name_ar: Optional[str] = None
    last_name_ar: Optional[str] = None
    profession: Optional[str] = None
    position: Optional[str] = None
    email: EmailStr
    contact_no: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    image: Optional[str] = None
    
    
class UserResponse(BaseModel):
    id: int
    first_name_en: str
    second_name_en: Optional[str] 
    last_name_en: str
    first_name_ar: Optional[str] = None
    second_name_ar: Optional[str] = None
    last_name_ar: Optional[str] = None
    user_name: str
    profession: Optional[str] = None
    position: Optional[str] = None
    email: EmailStr
    contact_no: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    image: Optional[str] = None
    upload_cv: Optional[str] = None
    role: Optional[UserRoleEnum]= UserRoleEnum.ADMIN
    
    class Config:
        orm_mode = True
        from_attributes = True 
        
        
class AllUserResponse(BaseModel):
    id: int
    first_name_en: str
    second_name_en: str
    last_name_en: str
    first_name_ar: Optional[str] = None
    second_name_ar: Optional[str] = None
    last_name_ar: Optional[str] = None
    user_name: str
    profession: Optional[str] = None
    position: Optional[str] = None
    email: EmailStr
    contact_no: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    image: Optional[str] = None
    upload_cv: Optional[str] = None
    role: Optional[UserRoleEnum]= UserRoleEnum.ADMIN
    
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
    contact_no: Optional[str] = None   
    
    
class AddUser(BaseModel):
    pass   
    
    
    
    
    
    
     
        
        
        
            
            
        
        
        
    
    
    
            
        
        
        
    
    
        
    
    
            
    
    
    
    