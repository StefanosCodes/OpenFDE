from fastapi import APIRouter, Depends

from app.auth import require_service_key
from app.routers import accounts, agent_results, calls, documents, tasks

v1_router = APIRouter(prefix="/v1", dependencies=[Depends(require_service_key)])
v1_router.include_router(accounts.router)
v1_router.include_router(calls.router)
v1_router.include_router(documents.router)
v1_router.include_router(tasks.router)
v1_router.include_router(agent_results.router)
