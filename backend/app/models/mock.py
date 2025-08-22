"""
Mock接口数据模型
"""

import enum

from sqlalchemy import JSON, Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class HTTPMethod(str, enum.Enum):
    """HTTP方法枚举"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class MockAPI(BaseModel):
    """Mock接口模型"""

    __tablename__ = "mock_apis"

    # 基本信息
    name = Column(String(255), nullable=False, comment="Mock接口名称")
    description = Column(Text, comment="接口描述")

    # 请求配置
    method = Column(Enum(HTTPMethod), nullable=False, comment="HTTP方法")
    path = Column(String(500), nullable=False, comment="接口路径")

    # 响应配置
    status_code = Column(Integer, default=200, comment="响应状态码")
    response_headers = Column(JSON, comment="响应头配置")
    response_body = Column(JSON, comment="响应体配置")
    response_template = Column(Text, comment="响应模板")

    # 状态管理
    is_active = Column(Boolean, default=True, comment="是否启用")
    version = Column(Integer, default=1, comment="版本号")
    
    # 分类关联
    category_id = Column(Integer, ForeignKey("categories.id"), comment="所属分类ID")
    
    # 关系定义
    category = relationship("Category", back_populates="mock_apis")

    def __repr__(self):
        return f"<MockAPI(id={self.id}, name='{self.name}', method='{self.method}', path='{self.path}')>"
