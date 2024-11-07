from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy import DECIMAL, Enum, Index, Table
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from enum import Enum as Pyenum

from core.config import settings

Base = declarative_base()

class UserRole(Pyenum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"
    

user_role_table = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


role_permission_table = Table(
    'role_permission', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)


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
    is_super_admin = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    roles = relationship('Role', secondary=user_role_table, back_populates='users')
    user_permissions = relationship("UserPermission", back_populates='users')
    files = relationship("File", back_populates="users")
    logs = relationship("Logs", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notifications", back_populates="user", cascade="all, delete-orphan")
    forget_password = relationship("ForgetPassword", back_populates="users")
    organizations = relationship("Organization", back_populates="users")
    branches = relationship("Branch", back_populates="users")


class ForgetPassword(Base):
    __tablename__ = "forget_password"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(Integer, nullable=True)
    otp_expires_at = Column(DateTime(timezone=True), nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    users = relationship("User", back_populates="forget_password")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), index=True, nullable=False)
    description = Column(String(64), nullable=True)
    is_delete = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    users = relationship('User', secondary=user_role_table, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permission_table, back_populates='roles')


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), index=True, nullable=False)  # Name of the permission (e.g., 'read', 'write')
    description = Column(String, nullable=True)  # Description of what the permission allows
    is_delete = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    roles = relationship('Role', secondary=role_permission_table, back_populates='permissions')


class UserPermission(Base):
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    users = relationship("User", back_populates="user_permissions")
    permissions = relationship("Permission")
    

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(64), index=True, nullable=False)
    name_ar = Column(String(64), index=True, nullable=True)
    commercial_id = Column(String(64), unique=True, nullable=False)
    location = Column(String(64), nullable=True)
    contact_no = Column(String(64), nullable=True)
    email = Column(String(64), index=True, unique=True, nullable=True)
    vat_no = Column(String(64), nullable=True)
    website = Column(String(255), nullable=True)
    instagram = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    others = Column(String(255), nullable=True)
    owner_name = Column(String(64), index=True, nullable=True)
    owner_contact_no = Column(String(64), nullable=True)
    owner_email = Column(String(64), nullable=True)
    logo = Column(String(255))
    logo_2 = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    tenant_id = Column(Integer, unique=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    users = relationship("User", back_populates="organizations")
    files = relationship("File", back_populates="organizations") 


class Branch(Base):
    __tablename__ = 'branches'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False) 
    location = Column(String(64), nullable=True)
    is_main_branch = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False) 
    
    creared_by = Column(Integer, ForeignKey('users.id'), nullable=False) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    users = relationship("User", back_populates="branches")
    
    
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)  
    file_path = Column(String(64), nullable=False)
    file_type = Column(String(64), nullable=False) 
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False) 
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    is_delete = Column(Boolean, default=False)
    
    organization_id = Column(Integer, ForeignKey("organizations.id")) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    organizations = relationship("Organization", back_populates="files")
    users = relationship("User", back_populates="files")


class Logs(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String(255), index=False)
    description = Column(Text, nullable=False) 
    is_delete = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    user = relationship("User", back_populates="logs") 
    
    
class Notifications(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=True)
    message = Column(Text, nullable=False) 
    data = Column(Text, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    is_delete = Column(Boolean, default=False)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    user = relationship("User", back_populates="notifications") 