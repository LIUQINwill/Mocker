"""
请求日志业务服务
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..models.log import RequestLog
from ..models.mock import MockAPI


class LogService:
    """请求日志服务类"""

    @staticmethod
    def create_log(
        db: Session,
        mock_api_id: Optional[int],
        request_method: str,
        request_path: str,
        request_headers: Optional[Dict[str, Any]] = None,
        request_body: Optional[Dict[str, Any]] = None,
        request_params: Optional[Dict[str, Any]] = None,
        response_status_code: Optional[int] = None,
        response_headers: Optional[Dict[str, Any]] = None,
        response_body: Optional[Dict[str, Any]] = None,
        response_time_ms: Optional[int] = None,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> RequestLog:
        """创建请求日志"""
        db_log = RequestLog(
            mock_api_id=mock_api_id,
            request_method=request_method,
            request_path=request_path,
            request_headers=request_headers,
            request_body=request_body,
            request_params=request_params,
            response_status_code=response_status_code,
            response_headers=response_headers,
            response_body=response_body,
            response_time_ms=response_time_ms,
            client_ip=client_ip,
            user_agent=user_agent,
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log

    @staticmethod
    def get_logs(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        mock_api_id: Optional[int] = None,
        method: Optional[str] = None,
        status_code: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> tuple[List[RequestLog], int]:
        """获取请求日志列表"""
        query = db.query(RequestLog)

        # 添加过滤条件
        if mock_api_id:
            query = query.filter(RequestLog.mock_api_id == mock_api_id)
        if method:
            query = query.filter(RequestLog.request_method == method)
        if status_code:
            query = query.filter(RequestLog.response_status_code == status_code)
        if start_date:
            query = query.filter(RequestLog.created_at >= start_date)
        if end_date:
            query = query.filter(RequestLog.created_at <= end_date)

        # 按时间倒序排列
        query = query.order_by(RequestLog.created_at.desc())

        # 获取总数
        total = query.count()

        # 分页查询
        items = query.offset(skip).limit(limit).all()

        return items, total

    @staticmethod
    def get_log(db: Session, log_id: int) -> Optional[RequestLog]:
        """获取单个请求日志"""
        return db.query(RequestLog).filter(RequestLog.id == log_id).first()

    @staticmethod
    def clear_logs(db: Session) -> int:
        """清空所有日志"""
        count = db.query(RequestLog).count()
        db.query(RequestLog).delete()
        db.commit()
        return count

    @staticmethod
    def get_stats(db: Session) -> Dict[str, Any]:
        """获取日志统计信息"""
        # 总请求数
        total_requests = db.query(RequestLog).count()

        # 今日请求数
        today = datetime.now().date()
        today_requests = (
            db.query(RequestLog)
            .filter(func.date(RequestLog.created_at) == today)
            .count()
        )

        # 成功率（2xx状态码）
        success_count = (
            db.query(RequestLog)
            .filter(
                and_(
                    RequestLog.response_status_code >= 200,
                    RequestLog.response_status_code < 300,
                )
            )
            .count()
        )
        success_rate = (
            (success_count / total_requests * 100) if total_requests > 0 else 0
        )

        # 平均响应时间
        avg_response_time = (
            db.query(func.avg(RequestLog.response_time_ms)).scalar() or 0
        )

        # 热门API（按请求次数排序）
        top_apis = (
            db.query(
                RequestLog.request_path,
                RequestLog.request_method,
                func.count(RequestLog.id).label("count"),
            )
            .group_by(RequestLog.request_path, RequestLog.request_method)
            .order_by(func.count(RequestLog.id).desc())
            .limit(5)
            .all()
        )

        # 方法统计
        method_stats = dict(
            db.query(RequestLog.request_method, func.count(RequestLog.id))
            .group_by(RequestLog.request_method)
            .all()
        )

        # 状态码统计
        status_stats = dict(
            db.query(RequestLog.response_status_code, func.count(RequestLog.id))
            .group_by(RequestLog.response_status_code)
            .all()
        )

        return {
            "total_requests": total_requests,
            "today_requests": today_requests,
            "success_rate": round(success_rate, 2),
            "avg_response_time": round(avg_response_time, 2),
            "top_apis": [
                {
                    "path": api.request_path,
                    "method": api.request_method,
                    "count": api.count,
                }
                for api in top_apis
            ],
            "method_stats": method_stats,
            "status_stats": {
                str(k): v for k, v in status_stats.items() if k is not None
            },
        }
