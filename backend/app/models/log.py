"""
请求日志数据模型
"""

from sqlalchemy import JSON, BigInteger, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class RequestLog(BaseModel):
    """请求日志模型"""

    __tablename__ = "request_logs"

    # 关联的Mock接口
    mock_api_id = Column(
        Integer, ForeignKey("mock_apis.id"), nullable=True, comment="关联的Mock接口ID"
    )

    # 请求信息
    request_method = Column(String(10), nullable=False, comment="请求方法")
    request_path = Column(String(500), nullable=False, comment="请求路径")
    request_headers = Column(JSON, comment="请求头")
    request_body = Column(JSON, comment="请求体")
    request_params = Column(JSON, comment="请求参数")

    # 响应信息
    response_status_code = Column(Integer, comment="响应状态码")
    response_headers = Column(JSON, comment="响应头")
    response_body = Column(JSON, comment="响应体")
    response_time_ms = Column(Integer, comment="响应时间(毫秒)")

    # 客户端信息
    client_ip = Column(String(45), comment="客户端IP")
    user_agent = Column(Text, comment="User Agent")

    # 关联关系
    mock_api = relationship("MockAPI", backref="request_logs")

    def __repr__(self):
        return f"<RequestLog(id={self.id}, method='{self.request_method}', path='{self.request_path}')>"
