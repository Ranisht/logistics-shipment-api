from fastapi import APIRouter
from app.api.v1.endpoints import health,shipments

api_router=APIRouter(prefix="/api/v1")
api_router.include_router(shipments.router)
api_router.include_router(health.router)