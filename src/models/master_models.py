from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, BigInteger, DECIMAL
from sqlalchemy.sql import func, text
from enum import Enum as Pyenum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
    
class UserStatus(Pyenum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    

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

# Many-to-Many Association Table for Module and SubscriptionPlans
module_subscription_plans_association = Table(
    'module_subscription_plans_association',
    Base.metadata,
    Column('module_id', Integer, ForeignKey('modules.id'), primary_key=True),
    Column('subscription_plan_id', Integer, ForeignKey('subscription_plans.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(64), index=True, unique=True, nullable=False)
    password = Column(String(255))
    contact_no = Column(String(20), index=True, unique=True, nullable=True)  
    email_verified_at = Column(DateTime(timezone=True), nullable=True)  
    status = Column(Enum(UserStatus, name="userstatus"), default=UserStatus.ACTIVE, nullable=False)
    remember_token = Column(String(255), nullable=True)
    is_loggedin = Column(Boolean, default=False)
    image = Column(String(255), nullable=True)
    is_super_admin = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    roles = relationship('Role', secondary=user_role_table, back_populates='users')
    user_permissions = relationship("UserPermission", back_populates='users')
    forget_password = relationship("ForgetPassword", back_populates="users")


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


class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    host = Column(String(255), index=True)
    db_name = Column(String(255), index=True)
    organization_name = Column(String(255), unique=True, index=True)
    status = Column(Boolean, default=True)
    is_shared = Column(Boolean, default=False)
    is_subscribed = Column(Boolean, default=False)
    user_count= Column(BigInteger, index=True, nullable=False, default=0)
    is_migrate = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    tenant_subscriptions = relationship("TenantSubscriptions", back_populates='tenant')

# Module Model
class Module(Base):
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(100), nullable=False, unique=True)  
    description = Column(String(255), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Many-to-Many Relationship with SubscriptionPlans
    subscription_plans = relationship(
        "SubscriptionPlans",
        secondary=module_subscription_plans_association,
        back_populates="modules"
    )
    # Relationships
    module_subscriptions = relationship("ModuleSubscription", back_populates="module")

# Enum for discount type
class DiscountType(Pyenum):
    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"

# Discount Offer Model
class DiscountOffer(Base):
    __tablename__ = 'discount_offers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(DiscountType), nullable=False) 
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    date_activated = Column(DateTime(timezone=True), nullable=False)
    date_deactivated = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relationships
    module_subscriptions = relationship("ModuleSubscription", back_populates="discount_offer")

# Enum for billing frequency
class BillingFrequencyType(Pyenum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    HALFYEARLY = "HALFYEARLY"
    YEARLY = "YEARLY"

# Enum for environment types
class EnvironmentType(Pyenum):
    PRODUCTION = "PRODUCTION"
    STAGING = "STAGING"
    DEVELOPMENT = "DEVELOPMENT"

# Subscription Plans Model
class SubscriptionPlans(Base):
    __tablename__ = 'subscription_plans'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    user_limit = Column(Integer, nullable=False)
    environment = Column(Enum(EnvironmentType), nullable=False)
    billing_frequency = Column(Enum(BillingFrequencyType), nullable=False)
    price = Column(DECIMAL(10, 5), nullable=False)
    discount_price = Column(DECIMAL(10, 5), nullable=True)
    date_activated = Column(DateTime(timezone=True), nullable=True)
    date_deactivated = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=False)
    is_delete = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Many-to-Many Relationship with Modules
    modules = relationship(
        "Module",
        secondary=module_subscription_plans_association,
        back_populates="subscription_plans"
    )
    # Relationships
    module_subscriptions = relationship("ModuleSubscription", back_populates="subscription_plan")

# Tenant Subscriptions Model
class TenantSubscriptions(Base):
    __tablename__ = 'tenant_subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    is_delete = Column(Boolean, default=False)

    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    subscription_plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=True)
    discount_offer_id = Column(Integer, ForeignKey('discount_offers.id'), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

    # Relationships
    tenant = relationship("Tenant", back_populates="tenant_subscriptions")
    module_subscriptions = relationship("ModuleSubscription", back_populates="tenant_subscription")
    payments = relationship("Payment", back_populates="tenant_subscription")
    subscription_plan = relationship("SubscriptionPlans")
    discount_offer = relationship("DiscountOffer")

# Enum for payment status
class PaymentStatus(Pyenum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    
# Enum for currency type
class CurrencyType(Pyenum):
    # East and Southeast Asia
    JPY = "JPY"  # Japanese Yen
    CNY = "CNY"  # Chinese Yuan
    KRW = "KRW"  # South Korean Won
    THB = "THB"  # Thai Baht
    IDR = "IDR"  # Indonesian Rupiah
    SGD = "SGD"  # Singapore Dollar
    MYR = "MYR"  # Malaysian Ringgit
    PHP = "PHP"  # Philippine Peso
    VND = "VND"  # Vietnamese Dong

    # South Asia
    INR = "INR"  # Indian Rupee
    BDT = "BDT"  # Bangladeshi Taka
    PKR = "PKR"  # Pakistani Rupee
    LKR = "LKR"  # Sri Lankan Rupee
    NPR = "NPR"  # Nepalese Rupee

    # Middle East and Arab World
    AED = "AED"  # UAE Dirham
    SAR = "SAR"  # Saudi Riyal
    QAR = "QAR"  # Qatari Riyal
    KWD = "KWD"  # Kuwaiti Dinar
    BHD = "BHD"  # Bahraini Dinar
    OMR = "OMR"  # Omani Rial
    ILS = "ILS"  # Israeli Shekel
    LBP = "LBP"  # Lebanese Pound
    EGP = "EGP"  # Egyptian Pound
    JOD = "JOD"  # Jordanian Dinar
    YER = "YER"  # Yemeni Rial
    IQD = "IQD"  # Iraqi Dinar
    SYP = "SYP"  # Syrian Pound

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), nullable=False, unique=True)  # Amazon Pay transaction ID
    amount = Column(DECIMAL(10, 2), nullable=False)  # Payment amount
    currency = Column(Enum(CurrencyType), nullable=False, default=CurrencyType.SAR.name)  # Currency code
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING.name)
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    amazon_order_reference_id = Column(String(100), nullable=True)  # Amazon order reference
    payment_method = Column(String(50), nullable=True)  # e.g., Credit Card, Balance
    card_last_four = Column(String(4), nullable=False)  # Last 4 digits of the card
    expiration_month = Column(Integer, nullable=False)  # Expiration month
    expiration_year = Column(Integer, nullable=False)  # Expiration year
    cardholder_name = Column(String(100), nullable=True)  # Optional cardholder name
    description = Column(String(255), nullable=True)  # Optional metadata or description
    is_delete = Column(Boolean, default=False)
    
    tenant_subscription_id = Column(Integer, ForeignKey('tenant_subscriptions.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    tenant_subscription = relationship("TenantSubscriptions", back_populates="payments")

# Module Subscription Model
class ModuleSubscription(Base):
    __tablename__ = 'module_subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    subscription_plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    tenant_subscription_id = Column(Integer, ForeignKey('tenant_subscriptions.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    discount_offer_id = Column(Integer, ForeignKey('discount_offers.id'), nullable=True)  # Optional

    # Relationships
    subscription_plan = relationship("SubscriptionPlans", back_populates="module_subscriptions")
    tenant_subscription = relationship("TenantSubscriptions", back_populates="module_subscriptions")
    module = relationship("Module", back_populates="module_subscriptions")
    discount_offer = relationship("DiscountOffer", back_populates="module_subscriptions")
 