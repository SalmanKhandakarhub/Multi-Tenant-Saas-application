from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import SessionLocal
from app.crud.crud_tenant import tenant_crud

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "").split(":")[0]
        db = SessionLocal()
        try:
            tenant = tenant_crud.get_by_domain(db, domain=host)
            if not tenant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tenant not found"
                    )
            request.state.tenant = tenant
            request.state.db = db
            response = await call_next(request)
            return response
        finally:
            db.close()