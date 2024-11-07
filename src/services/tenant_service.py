from typing import Type
from sqlalchemy.orm import Session

from models.tenant_models import *
from .base_service import BaseService


class TenantUserService(BaseService[User]):
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
    
    
class OrganizationService(BaseService[Organization]):
    def __init__(self, db: Session):
        super().__init__(Organization, db)