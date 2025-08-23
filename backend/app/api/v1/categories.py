"""
分类管理API路由
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.category import (
    BatchUpdateCategoryRequest,
    CategoryCreate,
    CategoryResponse,
    CategorySortRequest,
    CategoryStats,
    CategoryTree,
    CategoryUpdate,
)
from ...services.category_service import CategoryService

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取分类列表"""
    service = CategoryService(db)
    categories = service.get_categories(skip=skip, limit=limit)
    
    return [
        CategoryResponse(
            **category.__dict__,
            mock_count=category.mock_count,
            full_path=category.get_full_path()
        )
        for category in categories
    ]


@router.get("/tree", response_model=List[CategoryTree])
async def get_category_tree(db: Session = Depends(get_db)):
    """获取分类树形结构"""
    service = CategoryService(db)
    tree = service.get_category_tree()
    
    def build_tree_response(categories):
        result = []
        for category in categories:
            children = getattr(category, '_children', [])
            tree_item = CategoryTree(
                **category.__dict__,
                mock_count=category.mock_count,
                full_path=category.get_full_path(),
                children=build_tree_response(children) if children else []
            )
            result.append(tree_item)
        return result
    
    return build_tree_response(tree)


@router.get("/stats", response_model=CategoryStats)
async def get_category_stats(db: Session = Depends(get_db)):
    """获取分类统计信息"""
    service = CategoryService(db)
    stats = service.get_category_stats()
    return CategoryStats(**stats)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """创建分类"""
    service = CategoryService(db)
    
    try:
        category = service.create_category(category_data)
        return CategoryResponse(
            **category.__dict__,
            mock_count=category.mock_count,
            full_path=category.get_full_path()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/batch-update-mocks", status_code=status.HTTP_200_OK)
async def batch_update_mock_category(
    request: BatchUpdateCategoryRequest,
    db: Session = Depends(get_db)
):
    """批量更新接口分类"""
    service = CategoryService(db)
    
    try:
        success = service.batch_update_mock_category(
            request.category_id,
            request.mock_ids
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="批量更新失败"
            )
        
        return {"message": f"成功更新 {len(request.mock_ids)} 个接口的分类"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/sort", status_code=status.HTTP_200_OK)
async def update_category_sort(
    request: CategorySortRequest,
    db: Session = Depends(get_db)
):
    """更新分类排序"""
    service = CategoryService(db)
    
    success = service.update_category_sort(request.category_orders)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="排序更新失败"
        )
    
    return {"message": "分类排序更新成功"}


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """根据ID获取分类详情"""
    service = CategoryService(db)
    category = service.get_category_by_id(category_id)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"分类 {category_id} 不存在"
        )
    
    return CategoryResponse(
        **category.__dict__,
        mock_count=category.mock_count,
        full_path=category.get_full_path()
    )


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """更新分类"""
    service = CategoryService(db)
    
    try:
        category = service.update_category(category_id, category_data)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类 {category_id} 不存在"
            )
        
        return CategoryResponse(
            **category.__dict__,
            mock_count=category.mock_count,
            full_path=category.get_full_path()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """删除分类"""
    service = CategoryService(db)
    
    try:
        success = service.delete_category(category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分类 {category_id} 不存在"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )