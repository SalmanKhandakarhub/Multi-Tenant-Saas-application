from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from core.database_manager import get_tenant_db
from schemas.tenant.user_schemas import *
from services.tenant_service import TenantUserService
from utils.security import *

router = APIRouter()

@router.post('/tenant/login/',response_model=dict,include_in_schema=True)
def login_tenant(request:Request,user:OAuth2PasswordRequestForm=Depends(), 
    db: Session = Depends(get_tenant_db)):
    tenant_user_service = TenantUserService(db)
    try:
        tenant_user_data = tenant_user_service.get_one({"email" : user.username})
        if not tenant_user_data or not verify_password(user.password,tenant_user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
                )
        access_token = create_access_tocken(data={"sub":tenant_user_data.email}) 
        return{
            "message": "Login successfully",
            "access_token": access_token,
            "user": UserResponse.from_orm(tenant_user_data)
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) 