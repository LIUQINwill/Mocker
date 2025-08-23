/**
 * 分类管理组合函数
 */

import { ref, computed } from 'vue'
import { categoryApi } from '@/api/categories'
import { toast } from '@/composables/useToast'
import type {
  Category,
  CategoryTree,
  CategoryCreate,
  CategoryUpdate,
  CategoryStats,
  BatchUpdateCategoryRequest
} from '@/types/category'

// 全局状态管理，确保数据在组件间共享
const loading = ref(false)
const fetchLoading = ref(false)
const error = ref<string | null>(null)
const categories = ref<Category[]>([])
const categoryTree = ref<CategoryTree[]>([])
const stats = ref<CategoryStats | null>(null)

export function useCategories() {

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
    // 防止重复请求
    if (fetchLoading.value) {
      return
    }

    try {
      fetchLoading.value = true
      error.value = null
      
      const result = await categoryApi.getCategoryTree()
      
      // 验证和清理数据
      if (!Array.isArray(result)) {
        categoryTree.value = []
        return
      }
      
      const cleanResult = result.filter(category => {
        return category && 
          typeof category === 'object' && 
          'id' in category && 
          'name' in category &&
          category.name !== null &&
          category.name !== undefined
      })
      
      // 直接赋值，确保响应式更新
      categoryTree.value = cleanResult
      
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || '获取分类树失败'
      error.value = errorMessage
      console.error('获取分类树失败:', err)
      
      // 确保categoryTree是空数组
      categoryTree.value = []
    } finally {
      fetchLoading.value = false
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
      
      // 显示成功提示
      toast.success('创建分类成功', `分类"${newCategory.name}"已创建`)
      
      return newCategory
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || '创建分类失败'
      error.value = errorMessage
      console.error('创建分类失败:', err)
      
      // 显示错误提示
      toast.error('创建分类失败', errorMessage)
      
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
      
      // 显示成功提示
      toast.success('更新分类成功', `分类"${updatedCategory.name}"已更新`)
      
      return updatedCategory
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || '更新分类失败'
      error.value = errorMessage
      console.error('更新分类失败:', err)
      
      // 显示错误提示
      toast.error('更新分类失败', errorMessage)
      
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
      
      // 显示成功提示
      toast.success('删除分类成功', '分类已成功删除')
      
      return true
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || '删除分类失败'
      error.value = errorMessage
      console.error('删除分类失败:', err)
      
      // 显示错误提示
      toast.error('删除分类失败', errorMessage)
      
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
      
      // 确保categories是数组且每个元素都有效
      const validCategories = Array.isArray(categories) ? categories.filter(category => 
        category && 
        typeof category === 'object' && 
        'id' in category && 
        'name' in category &&
        category.name !== null &&
        category.name !== undefined
      ) : []
      
      for (const category of validCategories) {
        result.push({ ...category, level })
        if (category.children && Array.isArray(category.children) && category.children.length > 0) {
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
    fetchLoading,
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