from typing import Optional
from app.crud.base import CURDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate
from sqlalchemy.orm import Session

class CRUDTenant(CURDBase[Tenant, TenantCreate, TenantUpdate]):
    def get_by_domain(self, db: Session, *, domain: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.domain == domain).first()
    
    def create(self, db: Session, *, obj_in: TenantCreate) -> Tenant:
        # return super().create(db, obj_in=obj_in)
        db_obj = Tenant(
            name = obj_in.name,
            domain = obj_in.domain 
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    
tenant_crud = CRUDTenant(Tenant)