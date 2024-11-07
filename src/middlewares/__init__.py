from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.database_manager import get_master_db
from services.master_service import TenantService


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get('x-forwarded-host')
        tenant_service = TenantService(get_master_db())

        tenant = tenant_service.get_one({'host': host})
        if tenant:
            request.state.db = tenant.db_name
        else:
            request.state.db = None

        response = await call_next(request)
        return response