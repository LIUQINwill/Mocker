"""
请求日志API路由
"""

import math
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...schemas.log import LogStatsResponse, RequestLogList, RequestLogResponse
from ...services.log_service import LogService

router = APIRouter()


@router.get("/", response_model=RequestLogList, summary="获取请求日志列表")
def get_logs(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小"),
    mock_api_id: Optional[int] = Query(None, description="Mock接口ID"),
    method: Optional[str] = Query(None, description="请求方法"),
    status_code: Optional[int] = Query(None, description="响应状态码"),
    start_date: Optional[datetime] = Query(None, description="开始时间"),
    end_date: Optional[datetime] = Query(None, description="结束时间"),
    db: Session = Depends(get_db),
):
    """获取请求日志列表"""
    skip = (page - 1) * size
    logs, total = LogService.get_logs(
        db,
        skip=skip,
        limit=size,
        mock_api_id=mock_api_id,
        method=method,
        status_code=status_code,
        start_date=start_date,
        end_date=end_date,
    )

    pages = math.ceil(total / size) if total > 0 else 1

    return RequestLogList(items=logs, total=total, page=page, size=size, pages=pages)


@router.get("/{log_id}", response_model=RequestLogResponse, summary="获取请求日志详情")
def get_log(log_id: int, db: Session = Depends(get_db)):
    """获取单个请求日志详情"""
    log = LogService.get_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    return log


@router.delete("/", summary="清空所有日志")
def clear_logs(db: Session = Depends(get_db)):
    """清空所有请求日志"""
    count = LogService.clear_logs(db)
    return {"message": f"已清空 {count} 条日志"}


@router.get(
    "/stats/overview", response_model=LogStatsResponse, summary="获取日志统计信息"
)
def get_log_stats(db: Session = Depends(get_db)):
    """获取日志统计信息"""
    stats = LogService.get_stats(db)
    return LogStatsResponse(**stats)
