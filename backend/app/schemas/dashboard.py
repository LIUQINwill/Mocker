"""
仪表板数据模型
"""
from typing import List, Optional
from pydantic import BaseModel


class DashboardStats(BaseModel):
    """仪表板统计数据"""
    total_mocks: int = 0
    active_mocks: int = 0
    today_requests: int = 0
    success_rate: float = 0.0
    avg_response_time: float = 0.0


class RecentMockAPI(BaseModel):
    """最近的Mock接口"""
    id: int
    name: str
    method: str
    path: str
    is_active: bool
    created_at: str


class DashboardData(BaseModel):
    """仪表板完整数据"""
    stats: DashboardStats
    recent_mocks: List[RecentMockAPI]