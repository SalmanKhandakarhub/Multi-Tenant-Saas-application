from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum as Pyenum
from typing import Optional


#For Role and Permission 
class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    
    
class RoleResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        from_attributes=True
          
                        
class PermissionCreate(BaseModel):
    name: str
    description: str | None = None
    
    
class PermissionResponse(BaseModel):
    id: int
    name: str
    description: str | None
    
    class Config:
        orm_mode = True
        from_attributes=True
        
class AllRoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None 
    
    class Config:
        orm_mode = True
        from_attributes=True    
