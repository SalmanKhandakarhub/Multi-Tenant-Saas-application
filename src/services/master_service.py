from typing import Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.master_models import *
from .base_service import BaseService


class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)
        
    def assign_role_to_user(self, 
                            user_id: int, 
                            role_id: int):
        """Assign a role to a user."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError("Role not found.")
        
        user.roles.append(role)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all_users(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        exclude_user_id: Optional[int] = None,
        current_user_is_super_admin: bool = False
    ) -> List[User]:
        """Fetch all users with optional search by name and email."""
        query = self.db.query(User)
        #exclude the currently logged in user
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        if not current_user_is_super_admin:
            query = query.filter(User.is_super_admin == False)    
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    func.concat(User.first_name, " ", User.last_name).ilike(pattern),
                    User.email.like(pattern)
                )
            )  
            
        if status:
            try:
                query = query.filter(User.status == UserStatus(status)) 
            except:
                pass          
        total_count = query.count()
        new_query= query.order_by(User.created_at.desc())
        return new_query.offset(skip).limit(limit).all(), total_count
    
    
        
class RoleService(BaseService[Role]):
    def __init__(self, db: Session):
        super().__init__(Role, db)


class PermissionService(BaseService[Permission]):
    def __init__(self, db: Session):
        super().__init__(Permission, db)
        
        
class TenantService(BaseService[Tenant]):
    def __init__(self, db: Session):
        super().__init__(Tenant, db)
        
    def get_organization_by_name(self, organization_name: str):
        query = self.db.query(self.model).filter(func.lower(self.model.organization_name) == organization_name)
        return query.one_or_none()
        
           
class ForgetPasswordService(BaseService[ForgetPassword]):
    def __init__(self, db: Session):
        super().__init__(ForgetPassword, db)