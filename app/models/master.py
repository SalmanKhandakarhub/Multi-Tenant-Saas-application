from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, BigInteger, Enum, DECIMAL
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from enum import Enum as Pyenum



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

class BillingFrequencyType(Pyenum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class EnvironmentType(Pyenum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    
class SubscriptionProducts(Base):
    __tablename__ = 'subscription_products'
    
    id = Column(Integer, primary_key=True, index=True)
    api_product_id = Column(String(80), index=True)
    api_price_id = Column(String(80), index=True)
    environment = Column(Enum(EnvironmentType), nullable=False, server_default=EnvironmentType.PRODUCTION.name)
    billing_frequency = Column(Enum(BillingFrequencyType), nullable=False, server_default=BillingFrequencyType.MONTHLY.name)
    
    subscription_plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    subscription_plans = relationship("SubscriptionPlans", back_populates="subscription_products")
  
class SubscriptionPlans(Base):
    __tablename__ = 'subscription_plans'
    
    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(100), nullable=False)
    user_limit = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,5), nullable=False)
    max_discount_price = Column(DECIMAL(10,5), nullable=True)
    date_activated = Column(DateTime(timezone=True), nullable=True)
    date_deactivated = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    subscription_products = relationship("SubscriptionProducts", back_populates="subscription_plans")
  
class TenantSubscriptions(Base):
    __tablename__ = 'tenant_subscriptions'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=False)
    stripe_id = Column(String(100), nullable=False)  
    stripe_plan = Column(String(100), nullable=False) 
    quantity = Column(Integer, nullable=True) 
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    ends_at = Column(DateTime(timezone=True), nullable=True)
    stripe_product = Column(String(100), nullable=False) 
    stripe_webhook_status = Column(Integer, nullable=True)
    stripe_plan_id = Column(String(100), nullable=False)  
    
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  
    
    tenant = relationship("Tenant", back_populates="tenant_subscriptions")
    
class TenantSetting(Base):
    __tablename__ = 'tenant_settings'
    
    id = Column(Integer, primary_key=True, index=True)
    db_driver = Column(String(255), nullable=False)  # Database driver (e.g., MySQL, PostgreSQL)
    db_name = Column(String(255), nullable=False)  # Database name
    db_host = Column(String(255), nullable=False)  # Database host (e.g., localhost or IP)
    db_username = Column(String(255), nullable=False)  # Database username
    db_password = Column(String(255), nullable=False)  # Database password (store securely)
    client_id = Column(String(255), nullable=True)  # OAuth client ID
    client_secret = Column(String(255), nullable=True)  # OAuth client secret (store securely)
    redirect_url = Column(String(255), nullable=True)  # OAuth redirect URL
    workspace_id = Column(String(255), nullable=True) 
    
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    tenant = relationship("Tenant", back_populates="t_settings")
    user = relationship("User", back_populates="tenant_settings")

class Tenant(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    sub_domain = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)
    status = Column(Integer, nullable=True)
    is_shared = Column(Integer, nullable=True)
    is_subscribed = Column(Integer, nullable=True)
    user_count= Column(BigInteger, index=True, nullable=False, default=0)
    # customer_id
    
    creared_by = Column(Integer, ForeignKey('user.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    user = relationship("User", back_populates="tenant")
    t_settings = relationship("TenantSetting", back_populates='tenant', uselist=False)
    tenant_subscriptions = relationship("TenantSubscriptions", back_populates='tenant', uselist=False)
 
# Master super users tables 
class UserStatus(Pyenum):
    ACTIVE = 'active'
    INACTIVE = 'inactive' 
    
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(64), index=True, unique=True, nullable=False)
    password = Column(String(64))
    contact_no = Column(String(20), nullable=True)  
    email_verified_at = Column(DateTime(timezone=True), nullable=True)  
    ip = Column(String(45), nullable=True) 
    status = Column(Enum(UserStatus), nullable=False)
    remember_token = Column(String(255), nullable=True) 
    is_loggedin = Column(Integer, default=False)
    image = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)  
    
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    tenant = relationship("Tenant", back_populates="user")
    logs = relationship("Logs", back_populates="user")
    notifications = relationship("Notifications", back_populates="user")
    tenant_settings = relationship("TenantSetting", back_populates="user")