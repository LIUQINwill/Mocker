"""
Mock接口相关Schema
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..models.mock import HTTPMethod


class MockAPIBase(BaseModel):
    """Mock接口基础Schema"""

    name: str = Field(..., description="Mock接口名称")
    description: Optional[str] = Field(None, description="接口描述")
    method: HTTPMethod = Field(..., description="HTTP方法")
    path: str = Field(..., description="接口路径")
    status_code: int = Field(200, description="响应状态码")
    response_headers: Optional[Dict[str, str]] = Field(None, description="响应头配置")
    response_body: Optional[Dict[str, Any]] = Field(None, description="响应体配置")
    response_template: Optional[str] = Field(None, description="响应模板")
    is_active: bool = Field(True, description="是否启用")
    category_id: Optional[int] = Field(None, description="所属分类ID")


class MockAPICreate(MockAPIBase):
    """创建Mock接口Schema"""

    pass


class MockAPIUpdate(BaseModel):
    """更新Mock接口Schema"""

    name: Optional[str] = Field(None, description="Mock接口名称")
    description: Optional[str] = Field(None, description="接口描述")
    method: Optional[HTTPMethod] = Field(None, description="HTTP方法")
    path: Optional[str] = Field(None, description="接口路径")
    status_code: Optional[int] = Field(None, description="响应状态码")
    response_headers: Optional[Dict[str, str]] = Field(None, description="响应头配置")
    response_body: Optional[Dict[str, Any]] = Field(None, description="响应体配置")
    response_template: Optional[str] = Field(None, description="响应模板")
    is_active: Optional[bool] = Field(None, description="是否启用")
    category_id: Optional[int] = Field(None, description="所属分类ID")


class MockAPIResponse(MockAPIBase):
    """Mock接口响应Schema"""

    id: int = Field(..., description="接口ID")
    version: int = Field(..., description="版本号")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class MockAPIList(BaseModel):
    """Mock接口列表Schema"""

    items: List[MockAPIResponse] = Field(..., description="接口列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")
