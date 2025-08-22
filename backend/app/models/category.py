"""
接口分类数据模型
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
    """接口分类模型"""

    __tablename__ = "categories"

    # 基本信息
    name = Column(String(50), nullable=False, comment="分类名称")
    description = Column(String(200), comment="分类描述")
    
    # 层级关系
    parent_id = Column(Integer, ForeignKey("categories.id"), comment="父分类ID")
    sort_order = Column(Integer, default=0, comment="排序权重")
    
    # 状态管理
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    # 关系定义
    parent = relationship("Category", remote_side="Category.id", back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    mock_apis = relationship("MockAPI", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"

    @property
    def mock_count(self):
        """获取该分类下的接口数量"""
        return len(self.mock_apis) if self.mock_apis else 0

    def get_full_path(self):
        """获取分类的完整路径"""
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return " / ".join(path)