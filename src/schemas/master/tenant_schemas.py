from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum as Pyenum
from typing import Optional


#For Organizations and Tenent
class OrganizationCreate(BaseModel):
    name_en: str
    name_ar: Optional[str] = None
    commercial_id: str
    location: Optional[str] = None
    contact_no: str
    email: EmailStr
    vat_no: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    others: Optional[str] = None
    owner_name: str
    owner_contact_no: str
    owner_email: EmailStr
        
        
class TenantCreate(BaseModel):
    name: str
    sub_domain: Optional[str] = None
    status: Optional[bool] = True
    is_shared: Optional[int] = None
    is_subscribed: Optional[int] = None
    user_count: Optional[int] = 0
    

class OrganizationTenantCreate(BaseModel):
    organization: OrganizationCreate
    tenant: TenantCreate