"""
Mock接口业务服务
"""

from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..models.mock import MockAPI
from ..schemas.mock import MockAPICreate, MockAPIUpdate


class MockService:
    """Mock接口服务类"""

    @staticmethod
    def create_mock(db: Session, mock_data: MockAPICreate) -> MockAPI:
        """创建Mock接口"""
        db_mock = MockAPI(**mock_data.dict())
        db.add(db_mock)
        db.commit()
        db.refresh(db_mock)
        return db_mock

    @staticmethod
    def get_mock(db: Session, mock_id: int) -> Optional[MockAPI]:
        """获取单个Mock接口"""
        return db.query(MockAPI).filter(MockAPI.id == mock_id).first()

    @staticmethod
    def get_mocks(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None,
        method: Optional[str] = None,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> tuple[List[MockAPI], int]:
        """获取Mock接口列表"""
        query = db.query(MockAPI)

        # 添加过滤条件
        if is_active is not None:
            query = query.filter(MockAPI.is_active == is_active)
        if method:
            query = query.filter(MockAPI.method == method)
        if search:
            query = query.filter(
                MockAPI.name.contains(search) | MockAPI.path.contains(search)
            )
        if category_id is not None:
            if category_id == 0:  # 0 表示查询未分类的接口
                query = query.filter(MockAPI.category_id.is_(None))
            else:
                query = query.filter(MockAPI.category_id == category_id)

        # 获取总数
        total = query.count()

        # 分页查询
        items = query.offset(skip).limit(limit).all()

        return items, total

    @staticmethod
    def update_mock(
        db: Session, mock_id: int, mock_data: MockAPIUpdate
    ) -> Optional[MockAPI]:
        """更新Mock接口"""
        db_mock = db.query(MockAPI).filter(MockAPI.id == mock_id).first()
        if not db_mock:
            return None

        # 更新字段
        update_data = mock_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_mock, field, value)

        # 更新版本号
        db_mock.version += 1

        db.commit()
        db.refresh(db_mock)
        return db_mock

    @staticmethod
    def delete_mock(db: Session, mock_id: int) -> bool:
        """删除Mock接口"""
        db_mock = db.query(MockAPI).filter(MockAPI.id == mock_id).first()
        if not db_mock:
            return False

        db.delete(db_mock)
        db.commit()
        return True

    @staticmethod
    def toggle_mock(db: Session, mock_id: int) -> Optional[MockAPI]:
        """切换Mock接口启用状态"""
        db_mock = db.query(MockAPI).filter(MockAPI.id == mock_id).first()
        if not db_mock:
            return None

        db_mock.is_active = not db_mock.is_active
        db.commit()
        db.refresh(db_mock)
        return db_mock

    @staticmethod
    def find_matching_mock(db: Session, method: str, path: str) -> Optional[MockAPI]:
        """查找匹配的Mock接口"""
        return (
            db.query(MockAPI)
            .filter(
                and_(
                    MockAPI.method == method,
                    MockAPI.path == path,
                    MockAPI.is_active == True,
                )
            )
            .first()
        )
