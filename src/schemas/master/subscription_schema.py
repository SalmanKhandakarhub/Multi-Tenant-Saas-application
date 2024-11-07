# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime



# # 1. Base Schema
# class SubscriptionPlanBase(BaseModel):
#     plan_name: str
#     user_limit: int
#     price: float
#     max_discount_price: Optional[float] = None
#     date_activated: Optional[datetime] = None
#     date_deactivated: Optional[datetime] = None
#     is_active: bool = False
#     is_delete: bool = False

# # 2. Create Subscription Plan Schema
# class CreateSubscriptionPlan(SubscriptionPlanBase):
#     pass

# # 3. Update Subscription Plan Schema
# class UpdateSubscriptionPlan(BaseModel):
#     plan_name: Optional[str] = None
#     user_limit: Optional[int] = None
#     price: Optional[float] = None
#     max_discount_price: Optional[float] = None
#     date_activated: Optional[datetime] = None
#     date_deactivated: Optional[datetime] = None
#     is_active: Optional[bool] = None
#     is_delete: Optional[bool] = None

# # 4. Subscription Plan Schema for Retrieval
# class SubscriptionPlan(SubscriptionPlanBase):
#     id: int
#     created_at: datetime
#     updated_at: Optional[datetime] = None

#     class Config:
#         orm_mode = True

