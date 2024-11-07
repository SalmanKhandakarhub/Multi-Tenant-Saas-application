# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from core.database_manager import get_master_db
# from schemas.master.subscription_schema import CreateSubscriptionPlan, UpdateSubscriptionPlan
# from models.master_models import *
# from utils.security import *

# router = APIRouter()

# @router.post('/subscription/plan/create',response_model=dict,include_in_schema=True)
# def create_subscription_plan(request_data: CreateSubscriptionPlan,
#                              current_user: User = Depends(get_current_user),
#                              db: Session = Depends(get_master_db)):
#     pass

# @router.patch('/subscription/plan/update',response_model=dict,include_in_schema=True)
# def create_subscription_plan(request_data: UpdateSubscriptionPlan,
#                              current_user: User = Depends(get_current_user),
#                              db: Session = Depends(get_master_db)):
#     pass