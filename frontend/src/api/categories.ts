/**
 * 分类管理 API 客户端
 */

import { apiClient } from './client'
import type {
  Category,
  CategoryTree,
  CategoryCreate,
  CategoryUpdate,
  CategoryStats,
  BatchUpdateCategoryRequest,
  CategorySortRequest
} from '@/types/category'

export const categoryApi = {
  /**
   * 获取分类列表
   */
  async getCategories(params?: {
    skip?: number
    limit?: number
  }): Promise<Category[]> {
    const { data } = await apiClient.get('/api/v1/categories', { params })
    return data
  },

  /**
   * 获取分类树形结构
   */
  async getCategoryTree(): Promise<CategoryTree[]> {
    const { data } = await apiClient.get('/api/v1/categories/tree')
    return data
  },

  /**
   * 获取分类统计信息
   */
  async getCategoryStats(): Promise<CategoryStats> {
    const { data } = await apiClient.get('/api/v1/categories/stats')
    return data
  },

  /**
   * 根据ID获取分类详情
   */
  async getCategory(categoryId: number): Promise<Category> {
    const { data } = await apiClient.get(`/api/v1/categories/${categoryId}`)
    return data
  },

  /**
   * 创建分类
   */
  async createCategory(categoryData: CategoryCreate): Promise<Category> {
    const { data } = await apiClient.post('/api/v1/categories', categoryData)
    return data
  },

  /**
   * 更新分类
   */
  async updateCategory(categoryId: number, categoryData: CategoryUpdate): Promise<Category> {
    const { data } = await apiClient.put(`/api/v1/categories/${categoryId}`, categoryData)
    return data
  },

  /**
   * 删除分类
   */
  async deleteCategory(categoryId: number): Promise<void> {
    await apiClient.delete(`/api/v1/categories/${categoryId}`)
  },

  /**
   * 批量更新接口分类
   */
  async batchUpdateMockCategory(request: BatchUpdateCategoryRequest): Promise<{ message: string }> {
    const { data } = await apiClient.put('/api/v1/categories/batch-update-mocks', request)
    return data
  },

  /**
   * 更新分类排序
   */
  async updateCategorySort(request: CategorySortRequest): Promise<{ message: string }> {
    const { data } = await apiClient.put('/api/v1/categories/sort', request)
    return data
  }
}