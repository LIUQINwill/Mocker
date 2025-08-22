"""
Mock接口API路由
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...schemas.mock import MockAPICreate, MockAPIList, MockAPIResponse, MockAPIUpdate
from ...services.mock_service import MockService

router = APIRouter()


@router.post("/", response_model=MockAPIResponse, summary="创建Mock接口")
def create_mock(mock_data: MockAPICreate, db: Session = Depends(get_db)):
    """创建新的Mock接口"""
    try:
        mock = MockService.create_mock(db, mock_data)
        return mock
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=MockAPIList, summary="获取Mock接口列表")
def get_mocks(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    method: Optional[str] = Query(None, description="HTTP方法"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    db: Session = Depends(get_db),
):
    """获取Mock接口列表"""
    skip = (page - 1) * size
    mocks, total = MockService.get_mocks(
        db, skip=skip, limit=size, is_active=is_active, method=method, search=search, category_id=category_id
    )

    pages = math.ceil(total / size) if total > 0 else 1

    return MockAPIList(items=mocks, total=total, page=page, size=size, pages=pages)


@router.get("/{mock_id}", response_model=MockAPIResponse, summary="获取Mock接口详情")
def get_mock(mock_id: int, db: Session = Depends(get_db)):
    """获取单个Mock接口详情"""
    mock = MockService.get_mock(db, mock_id)
    if not mock:
        raise HTTPException(status_code=404, detail="Mock接口不存在")
    return mock


@router.put("/{mock_id}", response_model=MockAPIResponse, summary="更新Mock接口")
def update_mock(mock_id: int, mock_data: MockAPIUpdate, db: Session = Depends(get_db)):
    """更新Mock接口"""
    mock = MockService.update_mock(db, mock_id, mock_data)
    if not mock:
        raise HTTPException(status_code=404, detail="Mock接口不存在")
    return mock


@router.delete("/{mock_id}", summary="删除Mock接口")
def delete_mock(mock_id: int, db: Session = Depends(get_db)):
    """删除Mock接口"""
    success = MockService.delete_mock(db, mock_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mock接口不存在")
    return {"message": "删除成功"}


@router.post(
    "/{mock_id}/toggle", response_model=MockAPIResponse, summary="切换Mock接口状态"
)
def toggle_mock(mock_id: int, db: Session = Depends(get_db)):
    """切换Mock接口启用/禁用状态"""
    mock = MockService.toggle_mock(db, mock_id)
    if not mock:
        raise HTTPException(status_code=404, detail="Mock接口不存在")
    return mock
