from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.models import user
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from app.apiRoute import deps

router = APIRouter()

@router.get("/tenants/", response_model=List[Tenant])
def read_tenants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tenants.
    """
    if crud.user.is_superuser(current_user):
        tenants = crud.tenant.get_multi(db, skip=skip, limit=limit)
    else:
        tenants = [current_user.tenant]
    return tenants

@router.post("/tenants/", response_model=Tenant)
def create_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_in: TenantCreate,
    current_user: user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new tenant.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    tenant = crud.tenant.create(db, obj_in=tenant_in)
    return tenant

@router.put("/tenants/{tenant_id}", response_model=Tenant)
def update_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    tenant_in: TenantUpdate,
    current_user: user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a tenant.
    """
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    tenant = crud.tenant.update(db, db_obj=tenant, obj_in=tenant_in)
    return tenant

@router.get("/tenants/{tenant_id}", response_model=Tenant)
def read_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    current_user: user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get tenant by ID.
    """
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if not crud.user.is_superuser(current_user) and (current_user.tenant_id != tenant.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return tenant

@router.delete("/tenants/{tenant_id}", response_model=Tenant)
def delete_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: int,
    current_user: user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a tenant.
    """
    tenant = crud.tenant.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    tenant = crud.tenant.remove(db, id=tenant_id)
    return tenant