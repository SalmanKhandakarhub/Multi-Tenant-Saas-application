from pydantic import BaseModel

class TenantBase(BaseModel):
    name: str
    domain: str

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    pass

class TenantInDBBase(TenantBase):
    id: int

    class Config:
        orm_mode = True

class Tenant(TenantInDBBase):
    pass

class TenantInDB(TenantInDBBase):
    pass