from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timezone
import os

from core.database_manager import get_master_db
from utils.email_utils import send_password_reset_email
from schemas.master.user_schemas import *
from services.master_service import *
from utils.file_utils import get_uploaded_file
from utils.security import *

router = APIRouter()

@router.post('/signup', response_model=dict, include_in_schema=True)
def sign_up(request_data: UserCreate,
            db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    try:
        existing_user = user_service.get_one({"email": request_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email is already registered"
                )
        request_data.password = hash_password(request_data.password)
        created_user = user_service.create(request_data)
        user_data = UserResponse.from_orm(created_user)
        return {
            "message": "Registration successfully",
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

@router.get("/uploads/{filename}", include_in_schema=False)
def get_uploaded_file_route(filename: str):
    return get_uploaded_file(filename)


@router.post('/login', response_model=LoginResponse, include_in_schema=True)
def login(
          request: Request,  
          user:OAuth2PasswordRequestForm=Depends(), 
          db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    try:
        user_data = user_service.get_one({"email" : user.username})
        print(user_data)
        if not user_data or not verify_password(user.password, user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="",
                headers={"WWW-Authenticate": "Bearer"}
                )
            
        access_token = create_access_tocken(data={"sub": user_data.email})
        image_filename = os.path.basename(user_data.image) if user_data.image else None
        profile_image_url = (
            str(request.url_for("get_uploaded_file_route", filename=image_filename))
            if image_filename else None
        )
        user_response = UserResponse(
            id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            contact_no=user_data.contact_no,
            status=user_data.status,
            is_super_admin=user_data.is_super_admin,
            image=profile_image_url
        )
        return{
            "message": "",
            "access_token": access_token,
            "user": user_response
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
        
        
@router.post('/password/forget', response_model=dict, include_in_schema=True)  
def forget_password(request_data: GetCredential,
                    background_tasks: BackgroundTasks,  
                    db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    forget_password_service = ForgetPasswordService(db)
    try:
        user = user_service.get_one({"email": request_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        reset_token = generate_reset_token(user.id)
        reset_link = f"{settings.DOMAIN}/#/confirm-password?token={reset_token}"
        forget_password_data = {
            "user_id": user.id,
            "reset_token": reset_token,
            "reset_token_expires_at": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        forget_password_entry = forget_password_service.create(forget_password_data)
        
        subject = "Welcome to Our Platform"
        body = f"Please use the following link to login: {reset_link}"
        
        background_tasks.add_task(send_password_reset_email, user.email, subject, body)
        return {
            "message": "",
            "data": user.id
        }   
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# 2. Reset Password - PATCH Endpoint
@router.patch('/password/reset', response_model=dict, include_in_schema=True)
def reset_password(request_data: ForgetPasswordCreate, 
                   token: str, 
                   db: Session = Depends(get_master_db)):
    user_service = UserService(db)
    forget_password_service = ForgetPasswordService(db)
    try:
        forget_password_entry = forget_password_service.get_one({"reset_token": token})
        current_time = datetime.now(timezone.utc)
        if not forget_password_entry or forget_password_entry.reset_token_expires_at < current_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        user = user_service.get_by_id(forget_password_entry.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if request_data.password != request_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        password = hash_password(request_data.password)
        update_user = user_service.update(user, {"password": password})

        forget_password_service.delete(forget_password_entry.id)

        return {
            "message": "",
            "data": UserResponse.from_orm(update_user)
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )        