"""
接口分类 Schema 定义
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """分类基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    description: Optional[str] = Field(None, max_length=200, description="分类描述")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    sort_order: int = Field(0, description="排序权重")
    is_active: bool = Field(True, description="是否启用")


class CategoryCreate(CategoryBase):
    """创建分类请求模型"""
    pass


class CategoryUpdate(BaseModel):
    """更新分类请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="分类名称")
    description: Optional[str] = Field(None, max_length=200, description="分类描述")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    sort_order: Optional[int] = Field(None, description="排序权重")
    is_active: Optional[bool] = Field(None, description="是否启用")


class CategoryResponse(CategoryBase):
    """分类响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    mock_count: int = Field(0, description="该分类下的接口数量")
    full_path: str = Field("", description="分类完整路径")
    
    class Config:
        from_attributes = True


class CategoryTree(CategoryResponse):
    """分类树形结构模型"""
    children: List["CategoryTree"] = Field(default_factory=list, description="子分类列表")


class CategoryStats(BaseModel):
    """分类统计信息"""
    total_categories: int = Field(0, description="总分类数量")
    total_apis: int = Field(0, description="总接口数量")
    active_categories: int = Field(0, description="启用的分类数量")
    inactive_categories: int = Field(0, description="禁用的分类数量")


class BatchUpdateCategoryRequest(BaseModel):
    """批量更新分类请求模型"""
    category_id: Optional[int] = Field(None, description="目标分类ID，null表示未分类")
    mock_ids: List[int] = Field(..., description="接口ID列表")


class CategorySortRequest(BaseModel):
    """分类排序请求模型"""
    category_orders: List[dict] = Field(..., description="分类排序列表，格式：[{\"id\": 1, \"sort_order\": 1}]")


# 更新前向引用
CategoryTree.model_rebuild()