"""API v1路由"""

from fastapi import APIRouter
from app.api.v1 import projects, test, analyze, admin, database, platforms, users, dashboard, kols

api_router = APIRouter()

# 注册路由
api_router.include_router(projects.router)
api_router.include_router(test.router)
api_router.include_router(analyze.router)
api_router.include_router(admin.router)
api_router.include_router(database.router)
api_router.include_router(platforms.router, prefix="/platforms", tags=["platforms"])
api_router.include_router(users.router)
api_router.include_router(dashboard.router)
api_router.include_router(kols.router)

__all__ = ["api_router"]
