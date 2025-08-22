/**
 * 分类管理组合函数
 */

import { ref, computed } from 'vue'
import { categoryApi } from '@/api/categories'
import type {
  Category,
  CategoryTree,
  CategoryCreate,
  CategoryUpdate,
  CategoryStats,
  BatchUpdateCategoryRequest
} from '@/types/category'

export function useCategories() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const categories = ref<Category[]>([])
  const categoryTree = ref<CategoryTree[]>([])
  const stats = ref<CategoryStats | null>(null)

  /**
   * 获取分类列表
   */
  const fetchCategories = async (params?: { skip?: number; limit?: number }) => {
    try {
      loading.value = true
      error.value = null
      categories.value = await categoryApi.getCategories(params)
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '获取分类列表失败'
      console.error('获取分类列表失败:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取分类树形结构
   */
  const fetchCategoryTree = async () => {
    try {
      loading.value = true
      error.value = null
      categoryTree.value = await categoryApi.getCategoryTree()
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '获取分类树失败'
      console.error('获取分类树失败:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取分类统计信息
   */
  const fetchCategoryStats = async () => {
    try {
      loading.value = true
      error.value = null
      stats.value = await categoryApi.getCategoryStats()
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '获取统计信息失败'
      console.error('获取统计信息失败:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 创建分类
   */
  const createCategory = async (categoryData: CategoryCreate): Promise<Category | null> => {
    try {
      loading.value = true
      error.value = null
      const newCategory = await categoryApi.createCategory(categoryData)
      
      // 重新获取分类列表
      await fetchCategoryTree()
      
      return newCategory
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '创建分类失败'
      console.error('创建分类失败:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新分类
   */
  const updateCategory = async (categoryId: number, categoryData: CategoryUpdate): Promise<Category | null> => {
    try {
      loading.value = true
      error.value = null
      const updatedCategory = await categoryApi.updateCategory(categoryId, categoryData)
      
      // 重新获取分类列表
      await fetchCategoryTree()
      
      return updatedCategory
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '更新分类失败'
      console.error('更新分类失败:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 删除分类
   */
  const deleteCategory = async (categoryId: number): Promise<boolean> => {
    try {
      loading.value = true
      error.value = null
      await categoryApi.deleteCategory(categoryId)
      
      // 重新获取分类列表
      await fetchCategoryTree()
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '删除分类失败'
      console.error('删除分类失败:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 批量更新接口分类
   */
  const batchUpdateMockCategory = async (request: BatchUpdateCategoryRequest): Promise<boolean> => {
    try {
      loading.value = true
      error.value = null
      await categoryApi.batchUpdateMockCategory(request)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || '批量更新失败'
      console.error('批量更新失败:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 扁平化分类树，用于选择器等场景
   */
  const flattenedCategories = computed(() => {
    const flatten = (categories: CategoryTree[], level = 0): (CategoryTree & { level: number })[] => {
      const result: (CategoryTree & { level: number })[] = []
      
      for (const category of categories) {
        result.push({ ...category, level })
        if (category.children && category.children.length > 0) {
          result.push(...flatten(category.children, level + 1))
        }
      }
      
      return result
    }
    
    return flatten(categoryTree.value)
  })

  /**
   * 根据ID查找分类
   */
  const findCategoryById = (id: number): CategoryTree | null => {
    const findInTree = (categories: CategoryTree[]): CategoryTree | null => {
      for (const category of categories) {
        if (category.id === id) {
          return category
        }
        if (category.children && category.children.length > 0) {
          const found = findInTree(category.children)
          if (found) return found
        }
      }
      return null
    }
    
    return findInTree(categoryTree.value)
  }

  return {
    loading,
    error,
    categories,
    categoryTree,
    stats,
    flattenedCategories,
    fetchCategories,
    fetchCategoryTree,
    fetchCategoryStats,
    createCategory,
    updateCategory,
    deleteCategory,
    batchUpdateMockCategory,
    findCategoryById
  }
}