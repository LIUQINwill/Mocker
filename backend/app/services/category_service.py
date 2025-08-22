"""
分类管理服务
"""

from typing import List, Optional

from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Session, joinedload

from ..models import Category, MockAPI
from ..schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """分类管理服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """获取分类列表"""
        return (
            self.db.query(Category)
            .filter(Category.is_active == True)
            .order_by(Category.sort_order, Category.created_at)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_category_tree(self) -> List[Category]:
        """获取分类树形结构"""
        # 获取所有启用的分类
        categories = (
            self.db.query(Category)
            .options(joinedload(Category.mock_apis))
            .filter(Category.is_active == True)
            .order_by(Category.sort_order, Category.created_at)
            .all()
        )
        
        # 构建树形结构
        category_map = {cat.id: cat for cat in categories}
        tree = []
        
        for category in categories:
            if category.parent_id is None:
                tree.append(category)
            else:
                parent = category_map.get(category.parent_id)
                if parent:
                    if not hasattr(parent, '_children'):
                        parent._children = []
                    parent._children.append(category)
        
        return tree

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """根据ID获取分类"""
        return (
            self.db.query(Category)
            .options(joinedload(Category.mock_apis))
            .filter(Category.id == category_id, Category.is_active == True)
            .first()
        )

    def create_category(self, category_data: CategoryCreate) -> Category:
        """创建分类"""
        # 检查父分类是否存在
        if category_data.parent_id:
            parent = self.get_category_by_id(category_data.parent_id)
            if not parent:
                raise ValueError(f"父分类 {category_data.parent_id} 不存在")

        # 检查同级别下是否有重名分类
        existing = self.db.query(Category).filter(
            and_(
                Category.name == category_data.name,
                Category.parent_id == category_data.parent_id,
                Category.is_active == True
            )
        ).first()
        
        if existing:
            raise ValueError(f"同级别下已存在名为 '{category_data.name}' 的分类")

        # 创建分类
        category = Category(**category_data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """更新分类"""
        category = self.get_category_by_id(category_id)
        if not category:
            return None

        # 检查父分类是否有效
        if category_data.parent_id is not None:
            if category_data.parent_id == category_id:
                raise ValueError("分类不能将自己设为父分类")
            
            if category_data.parent_id != 0:
                parent = self.get_category_by_id(category_data.parent_id)
                if not parent:
                    raise ValueError(f"父分类 {category_data.parent_id} 不存在")

        # 更新字段
        for field, value in category_data.model_dump(exclude_unset=True).items():
            if field == "parent_id" and value == 0:
                value = None
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        """删除分类（软删除）"""
        category = self.get_category_by_id(category_id)
        if not category:
            return False

        # 检查是否有子分类
        children_count = self.db.query(Category).filter(
            and_(Category.parent_id == category_id, Category.is_active == True)
        ).count()
        
        if children_count > 0:
            raise ValueError("该分类下还有子分类，无法删除")

        # 检查是否有关联的接口
        mock_count = self.db.query(MockAPI).filter(MockAPI.category_id == category_id).count()
        if mock_count > 0:
            raise ValueError(f"该分类下还有 {mock_count} 个接口，请先移动这些接口")

        # 软删除
        category.is_active = False
        self.db.commit()
        return True

    def get_category_stats(self) -> dict:
        """获取分类统计信息"""
        total_categories = self.db.query(Category).count()
        active_categories = self.db.query(Category).filter(Category.is_active == True).count()
        total_apis = self.db.query(MockAPI).count()
        
        return {
            "total_categories": total_categories,
            "active_categories": active_categories,
            "inactive_categories": total_categories - active_categories,
            "total_apis": total_apis
        }

    def batch_update_mock_category(self, category_id: int, mock_ids: List[int]) -> bool:
        """批量更新接口分类"""
        # 验证分类是否存在
        if category_id != 0:  # 0 表示移除分类
            category = self.get_category_by_id(category_id)
            if not category:
                raise ValueError(f"分类 {category_id} 不存在")

        # 批量更新
        target_category_id = None if category_id == 0 else category_id
        updated_count = (
            self.db.query(MockAPI)
            .filter(MockAPI.id.in_(mock_ids))
            .update({"category_id": target_category_id}, synchronize_session=False)
        )
        
        self.db.commit()
        return updated_count > 0

    def update_category_sort(self, category_orders: List[dict]) -> bool:
        """更新分类排序"""
        try:
            for order_data in category_orders:
                category_id = order_data.get("id")
                sort_order = order_data.get("sort_order")
                
                if category_id and sort_order is not None:
                    self.db.query(Category).filter(Category.id == category_id).update(
                        {"sort_order": sort_order}, synchronize_session=False
                    )
            
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False