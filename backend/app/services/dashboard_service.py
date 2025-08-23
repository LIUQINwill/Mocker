"""
仪表板服务层
"""
from datetime import datetime, date
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models.mock import MockAPI
from ..models.log import RequestLog
from ..schemas.dashboard import DashboardStats, RecentMockAPI, DashboardData


class DashboardService:
    """仪表板服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self) -> DashboardStats:
        """获取仪表板统计数据"""
        # 获取总接口数
        total_mocks = self.db.query(MockAPI).count()
        
        # 获取活跃接口数
        active_mocks = self.db.query(MockAPI).filter(MockAPI.is_active == True).count()
        
        # 获取今日请求数
        today = date.today()
        today_requests = self.db.query(RequestLog).filter(
            func.date(RequestLog.created_at) == today
        ).count()
        
        # 计算成功率（状态码 200-299 为成功）
        success_rate = 0.0
        if today_requests > 0:
            success_count = self.db.query(RequestLog).filter(
                and_(
                    func.date(RequestLog.created_at) == today,
                    RequestLog.response_status_code >= 200,
                    RequestLog.response_status_code < 300
                )
            ).count()
            success_rate = (success_count / today_requests) * 100
        
        # 计算平均响应时间
        avg_response_time = 0.0
        response_time_query = self.db.query(
            func.avg(RequestLog.response_time_ms)
        ).filter(func.date(RequestLog.created_at) == today).scalar()
        
        if response_time_query:
            avg_response_time = float(response_time_query)
        
        return DashboardStats(
            total_mocks=total_mocks,
            active_mocks=active_mocks,
            today_requests=today_requests,
            success_rate=round(success_rate, 1),
            avg_response_time=round(avg_response_time, 1)
        )
    
    def get_recent_mocks(self, limit: int = 5) -> List[RecentMockAPI]:
        """获取最近创建的Mock接口"""
        mocks = self.db.query(MockAPI).order_by(
            MockAPI.created_at.desc()
        ).limit(limit).all()
        
        return [
            RecentMockAPI(
                id=mock.id,
                name=mock.name,
                method=mock.method,
                path=mock.path,
                is_active=mock.is_active,
                created_at=mock.created_at.isoformat() if mock.created_at else ""
            )
            for mock in mocks
        ]
    
    def get_dashboard_data(self) -> DashboardData:
        """获取仪表板完整数据"""
        stats = self.get_dashboard_stats()
        recent_mocks = self.get_recent_mocks()
        
        return DashboardData(
            stats=stats,
            recent_mocks=recent_mocks
        )