"""
API路由汇总
"""

from fastapi import APIRouter

from .v1 import categories, dashboard, logs, mocks, proxy

api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(mocks.router, prefix="/mocks", tags=["Mock接口管理"])
api_router.include_router(categories.router, prefix="/categories", tags=["分类管理"])
api_router.include_router(logs.router, prefix="/logs", tags=["请求日志"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["仪表板"])

# Mock代理服务路由（单独处理，不加前缀）
proxy_router = APIRouter()
proxy_router.include_router(proxy.router, tags=["Mock代理服务"])
