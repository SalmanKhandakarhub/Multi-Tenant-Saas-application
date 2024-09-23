from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy import DECIMAL, Enum, Index
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from enum import Enum as Pyenum


class UserRole(Pyenum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name_en = Column(String(64), index=True, nullable=False)
    second_name_en = Column(String(64), index=True, nullable=True)
    last_name_en = Column(String(64), index=True, nullable=False)
    first_name_ar = Column(String(64), nullable=True)
    second_name_ar = Column(String(64), nullable=True)
    last_name_ar = Column(String(64), nullable=True)
    user_name = Column(String(64), index=True, unique=True, nullable=False)
    profession = Column(String(64), index=True, nullable=False)
    position = Column(String(64), index=True, nullable=False)
    email = Column(String(64), index=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    contact_no = Column(String(20), nullable=True)
    birthday = Column(Date, nullable=True)
    country = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    image = Column(String(255), nullable=True)
    upload_cv = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    use_mfa = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), nullable=False)

    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    user_roles = relationship("UserRole", back_populates='user')
    user_permissions = relationship("UserPermission", back_populates='user')
    organization = relationship("Organization", back_populates="users")
    files = relationship("File", back_populates="users")
    logs = relationship("Logs", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notifications", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_user_email', 'email'),
        Index('ix_user_user_name', 'user_name'),
        Index('ix_user_organization_id', 'organization_id')
    )

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(64), nullable=False)
    name_ar = Column(String(64), nullable=True)
    commercial_id = Column(String(64), unique=True, nullable=False)
    location = Column(String(64), nullable=True)
    contact_no = Column(String(64), nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    vat_no = Column(String(64), nullable=True)
    website = Column(String(255), nullable=True)
    instagram = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    others = Column(String(255), nullable=True)
    owner_name = Column(String(64), nullable=False)
    owner_contact_no = Column(String(64), nullable=False)
    owner_email = Column(String(64), nullable=False)
    logo = Column(String(255))
    logo_2 = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    users = relationship("User", back_populates="organization")
    branches = relationship("Branch", back_populates="organization", cascade="all, delete-orphan")
    subscriptions = relationship("SubscriptionPlan", back_populates="organization", cascade="all, delete-orphan")
    files = relationship("File", back_populates="organization", cascade="all, delete-orphan")

class Branch(Base):
    __tablename__ = 'branches'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False) 
    is_main_branch = Column(Boolean, default=False)  
    
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    organizations = relationship("Organization", back_populates="branches")
     
class SubscriptionPlans(Base):
    __tablename__ = 'subscription_plans'
    
    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(100), nullable=False)
    user_limit = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,5), nullable=False)
    max_discount_price = Column(DECIMAL(10, 5), nullable=True)
    date_activated = Column(DateTime(timezone=True), nullable=True)
    date_deactivated = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Integer, nullable=True)
    
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    organization = relationship("Organization", back_populates="subscriptions")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    description = Column(String(64), nullable=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    users = relationship("User", secondary="user_roles", back_populates="roles") # Many-to-many relationship with users
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)  # Name of the permission (e.g., 'read', 'write')
    description = Column(String, nullable=True)  # Description of what the permission allows
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)  
    file_path = Column(String(64), nullable=False)
    file_type = Column(String(64), nullable=False) 
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False) 
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    
    organization_id = Column(Integer, ForeignKey("organizations.id")) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    organizations = relationship("Organization", back_populates="files")
    users = relationship("User", back_populates="files")

class Logs(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String(255), index=False)
    description = Column(Text, nullable=False) 
    #type_id
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    user = relationship("User", back_populates="logs") 
    
class Notifications(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=True)
    message = Column(Text, nullable=False) 
    data = Column(Text, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    user = relationship("User", back_populates="notifications") 