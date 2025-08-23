/**
 * 分类相关的TypeScript类型定义
 */

export interface Category {
  id: number
  name: string
  description?: string
  parent_id?: number
  sort_order: number
  is_active: boolean
  created_at: string
  updated_at: string
  mock_count: number
  full_path: string
}

export interface CategoryTree extends Category {
  children: CategoryTree[]
}

export interface CategoryCreate {
  name: string
  description?: string
  parent_id?: number
  sort_order?: number
  is_active?: boolean
}

export interface CategoryUpdate {
  name?: string
  description?: string
  parent_id?: number
  sort_order?: number
  is_active?: boolean
}

export interface CategoryStats {
  total_categories: number
  total_apis: number
  active_categories: number
  inactive_categories: number
}

export interface BatchUpdateCategoryRequest {
  category_id: number | null
  mock_ids: number[]
}

export interface CategorySortRequest {
  category_orders: Array<{
    id: number
    sort_order: number
  }>
}

export interface CategoryResponse {
  id: number
  name: string
  description?: string
  parent_id?: number
  sort_order: number
  is_active: boolean
  created_at: string
  updated_at: string
  mock_count: number
  full_path: string
}