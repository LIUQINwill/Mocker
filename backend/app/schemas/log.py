"""
请求日志相关Schema
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RequestLogResponse(BaseModel):
    """请求日志响应Schema"""

    id: int = Field(..., description="日志ID")
    mock_api_id: Optional[int] = Field(None, description="关联的Mock接口ID")

    # 请求信息
    request_method: str = Field(..., description="请求方法")
    request_path: str = Field(..., description="请求路径")
    request_headers: Optional[Dict[str, Any]] = Field(None, description="请求头")
    request_body: Optional[Dict[str, Any]] = Field(None, description="请求体")
    request_params: Optional[Dict[str, Any]] = Field(None, description="请求参数")

    # 响应信息
    response_status_code: Optional[int] = Field(None, description="响应状态码")
    response_headers: Optional[Dict[str, Any]] = Field(None, description="响应头")
    response_body: Optional[Dict[str, Any]] = Field(None, description="响应体")
    response_time_ms: Optional[int] = Field(None, description="响应时间(毫秒)")

    # 客户端信息
    client_ip: Optional[str] = Field(None, description="客户端IP")
    user_agent: Optional[str] = Field(None, description="User Agent")

    # 时间信息
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class RequestLogList(BaseModel):
    """请求日志列表Schema"""

    items: List[RequestLogResponse] = Field(..., description="日志列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")


class LogStatsResponse(BaseModel):
    """日志统计响应Schema"""

    total_requests: int = Field(..., description="总请求数")
    today_requests: int = Field(..., description="今日请求数")
    success_rate: float = Field(..., description="成功率")
    avg_response_time: float = Field(..., description="平均响应时间")
    top_apis: List[Dict[str, Any]] = Field(..., description="热门API")
    method_stats: Dict[str, int] = Field(..., description="方法统计")
    status_stats: Dict[str, int] = Field(..., description="状态码统计")
