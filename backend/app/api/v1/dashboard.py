"""
仪表板API路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...schemas.dashboard import DashboardData, DashboardStats
from ...services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/stats", response_model=DashboardData)
async def get_dashboard_data(
    db: Session = Depends(get_db)
) -> DashboardData:
    """
    获取仪表板数据
    
    返回：
    - stats: 统计数据（总接口数、今日请求数、成功率、平均响应时间）
    - recent_mocks: 最近创建的Mock接口列表
    """
    service = DashboardService(db)
    return service.get_dashboard_data()


@router.get("/stats/summary", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db)
) -> DashboardStats:
    """
    获取仪表板统计数据
    
    返回统计数据：
    - total_mocks: 总接口数
    - active_mocks: 活跃接口数
    - today_requests: 今日请求数
    - success_rate: 成功率
    - avg_response_time: 平均响应时间
    """
    service = DashboardService(db)
    return service.get_dashboard_stats()