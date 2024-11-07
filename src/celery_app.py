from celery import Celery

from core.config import settings
from src.commands.create_tenant_database import create_tenant_database

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,  # Redis or RabbitMQ broker URL
    backend=settings.CELERY_RESULT_BACKEND,  # Result backend (optional)
)

# Celery configuration
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery.task(bind=True, name="celery_app.create_tenant_database_task")
def create_tenant_database_task(self, tenant_data: dict, user_data: dict):
    """
    Background task for creating tenant database and running migrations.
    """
    try:
        # Call the create_tenant_database function
        create_tenant_database(tenant_data, user_data)
    except Exception as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)
