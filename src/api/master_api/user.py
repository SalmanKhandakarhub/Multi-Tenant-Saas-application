import os
from math import ceil
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Request,
    status,
    UploadFile,
)
from sqlalchemy.orm import Session

from celery_app import create_tenant_database_task
from core.config import settings
from core.database_manager import get_master_db
from utils.file_utils import get_uploaded_file
from schemas.master.role_permission_schenas import (
    Optional,
    RoleCreate,
    RoleResponse,
    AllRoleResponse,
    PermissionCreate,
    PermissionResponse,
)
from schemas.master.user_schemas import (
    AddUser,
    AllUserResponse,
    ChangePasswordCreate,
    StatusUpdateResponse,
    UpdateStatus,
    UserResponse,
    UserUpdate
)
from services.master_service import (
    PermissionService,
    RoleService,
    TenantService,
    UserService
)
from utils.security import (
    User,
    get_current_user,
    hash_password,
    verify_password
)

router = APIRouter()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.get('/profile', response_model=dict, include_in_schema=True)
def get_current_user_details(current_user: User=Depends(get_current_user),
                 db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    try:
        users = user_service.get_by_id(current_user.id)
        user_data = UserResponse.from_orm(users)
        return {
            "message": "Data fetched successfully",
            "data": user_data
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
            )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )


@router.patch('/update', response_model=dict, include_in_schema=True)
def update_user(request_data: UserUpdate, 
                  current_user: User = Depends(get_current_user), 
                  db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    try:
        users = user_service.get_by_id(current_user.id)
        updated_user = user_service.update(users, request_data.dict(exclude_unset=True))
        user_data = UserResponse.from_orm(updated_user)
        return {
            "message": "User status updated successfully", 
            "data": user_data
            }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put('/password/update', response_model=dict, include_in_schema=True)
def change_password(request_data: ChangePasswordCreate,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_master_db),):
    user_service = UserService(db)
    try:
        users = user_service.get_by_id(current_user.id)
        
        if not verify_password(request_data.old_password, users.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect"
            )
            
        password = hash_password(request_data.password)
        update_user = user_service.update(users, {"password": password})
        
        return {
            "message": "Password reset successfully",
            "data": UserResponse.from_orm(update_user)
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        

@router.get("/uploads/{filename}", include_in_schema=False)
def get_uploaded_file_route(filename: str):
    return get_uploaded_file(filename)


@router.put('/image/update', response_model=dict, include_in_schema=True)
def change_image(
                request: Request,
                file: UploadFile = File(...), 
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    try:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only JPEG or PNG is allowed."
            )
            
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid4()}.{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        file_content = file.file.read() 
        with open(file_path, "wb") as f:
            f.write(file_content)
            
        updated_user = user_service.update(current_user, {"image": file_path})
        image_url = request.url_for("get_uploaded_file_route", filename=unique_filename)
        
        return {
            "message": "Image updated successfully",
            "image_url": str(image_url),
            "data": updated_user.id
        }
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/users', response_model=dict, include_in_schema=True)
def get_all_user(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_master_db),
    search: Optional[str] = Query(None),
    user_status: Optional[str] = Query(None),
    page: int = Query(1),
    page_size: int = Query(10)
):
    user_service = UserService(db)
    try:
        if not current_user.is_super_admin:
            current_user_is_super_admin= False
        else:
            current_user_is_super_admin= True
        offset = (page - 1) * page_size
        users,total_count = user_service.get_all_users(search=search, skip=offset, limit=page_size, exclude_user_id=current_user.id, status=user_status, current_user_is_super_admin=current_user_is_super_admin)
        user_data = []
        for user in users:
            filename = user.image if user.image else None
            if filename:
                filename = os.path.basename(filename) 
                profile_image_url = request.url_for("get_uploaded_file_route", filename=filename)
            else:
                profile_image_url = None
            
            user_response = AllUserResponse(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                contact_no=user.contact_no,
                status=user.status,
                is_super_admin=user.is_super_admin,
                image=str(profile_image_url)  
            )
            user_data.append(user_response)
        page_count = ceil(total_count/page_size)
        return {
            "data": user_data,
            "total": len(user_data),
            "page": page,
            "total_pages": page_count
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch('/status/update', response_model=dict, include_in_schema=True)
def update_status(request_data: UpdateStatus, 
                  current_user: User = Depends(get_current_user), 
                  db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    try:
        if current_user.is_super_admin != True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User status is not active. Cannot create roles."
            )
        
        user = user_service.get_by_id(request_data.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        print("Updating status with:", str(request_data.status.name))
        
        update_user = user_service.update(user, {"status": str(request_data.status.name)})
        user_data = StatusUpdateResponse.from_orm(update_user)
        return {
            "message": "User status updated successfully", 
            "data": user_data}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post('/role/add', response_model=dict, include_in_schema=True)
def add_roles(request_data: RoleCreate,
              current_user: User=Depends(get_current_user), 
              db: Session = Depends(get_master_db)):
    role_service = RoleService(db)
    try:
        if current_user.is_super_admin != True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User status is not active. Cannot create roles."
            )

        existing_role = role_service.get_one({"name": request_data.name})
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already exists."
            )
            
        new_role = role_service.create(request_data)
        role_data = RoleResponse.from_orm(new_role)
        return {
            "message": "Role created successfully",
            "data": role_data
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
        

@router.get('/roles',response_model=dict,include_in_schema=True)
def get_roles(current_user: User=Depends(get_current_user),
                 db: Session = Depends(get_master_db)):  
    role_service=RoleService(db)
    try:
        if current_user.is_super_admin !=True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This user is not allowed to see roles."
            )
        roles=role_service.get_all()   
        roles_data = [AllRoleResponse.from_orm(role) for role in roles]
        return {
            "data": roles_data
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
            )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
        
        
@router.post('/permission/add', response_model=dict, include_in_schema=True)
def add_permission(request_data: PermissionCreate,
              current_user: User=Depends(get_current_user),
              db: Session = Depends(get_master_db)):
    permission_service = PermissionService(db)
    try:
        if current_user.is_super_admin != True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User status is not active. Cannot create roles."
            )

        existing_role = permission_service.get_one({"name": request_data.name})
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission already exists."
            )
            
        new_permission = permission_service.create(request_data)
        permission_data = PermissionResponse.from_orm(new_permission)
        return {
            "message": "Permission created successfully",
            "data": permission_data
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )


@router.post('/tenant/create', response_model=dict, include_in_schema=True)
def create_user(request_data: AddUser,
                current_user: User = Depends(get_current_user), 
                db: Session = Depends(get_master_db)):
    tenant_service = TenantService(db)
    try:
        if not current_user.is_super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="You do not have permission to perform this action."
            )
        org_name_normalized = request_data.organization_name.lower().replace(" ", "_")
        existing_organization = tenant_service.get_organization_by_name(org_name_normalized)
        if existing_organization:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Organization already exists."
            )
        user_data = request_data.dict()
        user_data['sub_domain'] = org_name_normalized
        new_tenant_data = {
            "host": f"{request_data.organization_name.lower()}.{settings.DOMAIN}",
            "db_name": f"{org_name_normalized}_rinku",
            "status": True,
            "organization_name": request_data.organization_name
        }
        tenant = tenant_service.create(new_tenant_data)
        user_data['tenant_id'] = tenant.id

        create_tenant_database_task.delay(new_tenant_data, user_data)
        
        return {
            "message": "Registration successful. Password has been sent to your email.",
            "data": {}
        }

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
              