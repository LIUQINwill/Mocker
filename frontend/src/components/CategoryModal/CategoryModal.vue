<template>
  <div 
    v-show="visible" 
    class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50" 
    @click.self="handleClose"
  >
    <div class="flex items-center justify-center min-h-screen p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
        <!-- 标题栏 -->
        <div class="flex-shrink-0 px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-xl font-semibold text-gray-900">分类管理</h2>
            <div class="flex items-center space-x-2">
              <!-- 紧急重置按钮 -->
              <button
                @click="emergencyReset"
                class="text-xs text-gray-400 hover:text-orange-600 transition-colors px-2 py-1 border border-gray-300 rounded"
                title="紧急重置（如果界面卡死请点击）"
                v-if="fetchLoading || loading"
              >
                重置
              </button>
              <!-- 关闭按钮 -->
              <button
                @click="handleClose"
                class="text-gray-400 hover:text-gray-600 transition-colors"
                title="关闭"
              >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 主体内容 -->
        <div class="flex-1 flex overflow-hidden">
          <!-- 左侧表单区域 -->
          <div class="w-1/2 p-6 border-r border-gray-200">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ editingCategory ? '编辑分类' : '新增分类' }}
            </h3>

            <form @submit.prevent="handleSubmit" class="space-y-4">
              <!-- 分类名称 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  分类名称 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.name"
                  type="text"
                  required
                  placeholder="请输入分类名称"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  :disabled="loading"
                />
              </div>

              <!-- 分类描述 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  分类描述
                </label>
                <textarea
                  v-model="form.description"
                  rows="3"
                  placeholder="请输入分类描述（可选）"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  :disabled="loading"
                />
              </div>

              <!-- 父分类选择 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  父分类
                </label>
                <select
                  v-model="form.parent_id"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  :disabled="loading"
                >
                  <option :value="null">无（作为顶级分类）</option>
                  <option 
                    v-for="category in availableParentCategories"
                    :key="category.id" 
                    :value="category.id"
                    :disabled="category.id === editingCategory?.id"
                  >
                    {{ '　'.repeat(category.level) }}{{ category.name }}
                  </option>
                </select>
              </div>

              <!-- 操作按钮 -->
              <div class="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  @click="handleCancel"
                  class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  :disabled="loading"
                >
                  取消
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  :disabled="loading || !form?.name?.trim()"
                >
                  <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ loading ? '保存中...' : (editingCategory ? '更新' : '添加') }}
                </button>
              </div>
            </form>
          </div>

          <!-- 右侧分类列表区域 -->
          <div class="w-1/2 flex flex-col">
            <!-- 列表标题 -->
            <div class="flex-shrink-0 px-6 py-4 border-b border-gray-200">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900">现有分类</h3>
                <button
                  @click="refreshCategories"
                  :disabled="fetchLoading"
                  class="text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50 transition-colors"
                  title="刷新分类列表"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- 分类列表内容 -->
            <div class="flex-1 overflow-auto">
              <!-- 加载状态 -->
              <div v-if="fetchLoading" class="p-8 text-center">
                <svg class="animate-spin h-8 w-8 text-blue-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p class="text-gray-600">正在加载分类...</p>
              </div>

              <!-- 错误状态 -->
              <div v-else-if="error" class="p-8 text-center">
                <svg class="h-12 w-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <p class="text-red-600 mb-4">{{ error }}</p>
                <button
                  @click="refreshCategories"
                  class="text-sm text-blue-600 hover:text-blue-800"
                >
                  重新加载
                </button>
              </div>

              <!-- 空状态 -->
              <div v-else-if="validCategories.length === 0" class="p-8 text-center">
                <svg class="h-12 w-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002 2H5a2 2 0 00-2-2z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h2a2 2 0 012 2v0H8v0z"></path>
                </svg>
                <p class="text-gray-600">暂无分类</p>
                <p class="text-sm text-gray-500 mt-2">添加您的第一个分类吧</p>
              </div>

              <!-- 分类列表 -->
              <div v-else class="py-2">
                <CategoryManageItem
                  v-for="category in validCategories"
                  :key="category.id"
                  :category="category"
                  :level="0"
                  @edit="handleEditCategory"
                  @delete="handleDeleteCategory"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useCategories } from '@/composables/useCategories'
import CategoryManageItem from './CategoryManageItem.vue'
import type { CategoryTree, CategoryCreate, CategoryUpdate } from '@/types/category'

interface Props {
  visible: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'updated'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 使用分类管理组合函数
const {
  loading,
  fetchLoading,
  error,
  categoryTree,
  flattenedCategories,
  fetchCategoryTree,
  createCategory,
  updateCategory,
  deleteCategory
} = useCategories()

// 表单数据
const form = ref<{
  name: string
  description: string
  parent_id: number | null
}>({
  name: '',
  description: '',
  parent_id: null
})

// 监听form变化（保留用于排查问题）
// watch(form, (newForm) => {
//   console.log('form数据变化:', newForm)
// }, { deep: true })

// 编辑状态
const editingCategory = ref<CategoryTree | null>(null)

// 有效的分类列表（过滤掉无效数据）
const validCategories = computed(() => {
  if (!categoryTree.value || !Array.isArray(categoryTree.value)) {
    return []
  }
  
  // 简化过滤逻辑，只检查最基本的属性
  const filtered = categoryTree.value.filter(category => {
    return category && 
           category.id !== undefined && category.id !== null &&
           category.name !== undefined && category.name !== null
  })
  
  return filtered
})

// 可选择的父分类（排除当前编辑的分类及其子分类）
const availableParentCategories = computed(() => {
  if (!editingCategory.value) {
    return flattenedCategories.value
  }

  // 获取当前编辑分类的所有子分类ID
  const getChildrenIds = (category: CategoryTree): number[] => {
    let ids = [category.id]
    if (category.children && category.children.length > 0) {
      category.children.forEach(child => {
        ids.push(...getChildrenIds(child))
      })
    }
    return ids
  }

  const excludedIds = getChildrenIds(editingCategory.value)
  
  return flattenedCategories.value.filter(category => 
    !excludedIds.includes(category.id)
  )
})

// 重置表单
const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    parent_id: null
  }
  editingCategory.value = null
}

// 紧急重置函数（用于解决界面卡死问题）
const emergencyReset = () => {
  try {
    // 强制重置所有状态
    loading.value = false
    fetchLoading.value = false
    error.value = null
    
    // 重置表单
    resetForm()
    
    // 清空分类数据
    categoryTree.value = []
  } catch (err) {
    console.error('紧急重置失败:', err)
  }
}

// 处理关闭
const handleClose = () => {
  try {
    resetForm()
    // 强制重置所有loading状态，确保窗口能够关闭
    loading.value = false
    fetchLoading.value = false
    error.value = null
    emit('close')
  } catch (err) {
    console.error('关闭窗口失败:', err)
    // 即使出错也要强制关闭
    emit('close')
  }
}

// 处理取消
const handleCancel = () => {
  resetForm()
}

// 处理表单提交
const handleSubmit = async () => {
  // 确保form.value存在并且有name属性
  if (!form.value || !form.value.name || !form.value.name.trim()) {
    return
  }

  // 防止重复提交
  if (loading.value) {
    return
  }

  try {
    const categoryData = {
      name: form.value.name.trim(),
      description: form.value.description?.trim() || undefined,
      parent_id: form.value.parent_id || undefined
    }

    if (editingCategory.value) {
      // 更新分类
      const result = await updateCategory(editingCategory.value.id, categoryData as CategoryUpdate)
      if (result) {
        resetForm()
        emit('updated')
      }
    } else {
      // 创建分类
      const result = await createCategory(categoryData as CategoryCreate)
      if (result) {
        resetForm()
        emit('updated')
      }
    }
  } catch (err) {
    console.error('提交表单失败:', err)
    // 确保loading状态正确重置
    loading.value = false
  }
}

// 处理编辑分类
const handleEditCategory = (category: CategoryTree) => {
  editingCategory.value = category
  form.value = {
    name: category.name,
    description: category.description || '',
    parent_id: category.parent_id || null
  }
}

// 处理删除分类
const handleDeleteCategory = async (category: CategoryTree) => {
  const confirmMessage = category.mock_count > 0 
    ? `确定要删除分类"${category.name}"吗？该分类下有 ${category.mock_count} 个接口，删除后这些接口将变为未分类状态。`
    : `确定要删除分类"${category.name}"吗？`

  if (confirm(confirmMessage)) {
    const result = await deleteCategory(category.id)
    if (result) {
      // 如果删除的是正在编辑的分类，重置表单
      if (editingCategory.value?.id === category.id) {
        resetForm()
      }
      emit('updated')
    }
  }
}

// 刷新分类列表
const refreshCategories = async () => {
  try {
    await fetchCategoryTree()
  } catch (err) {
    console.error('刷新分类列表失败:', err)
  }
}

// 监听弹窗显示状态
watch(() => props.visible, async (visible) => {
  if (visible) {
    // 弹窗打开时加载分类列表
    try {
      await fetchCategoryTree()
    } catch (err) {
      console.error('加载分类树失败:', err)
    }
    // 确保DOM更新后聚焦到名称输入框
    await nextTick()
    try {
      const nameInput = document.querySelector('input[type="text"]') as HTMLInputElement
      if (nameInput) {
        nameInput.focus()
      }
    } catch (err) {
      console.error('聚焦输入框失败:', err)
    }
  } else {
    // 弹窗关闭时重置表单
    resetForm()
  }
}, { immediate: false })

// 组件挂载时不自动加载，由watch处理
// onMounted(() => {
//   console.log('CategoryModal mounted')
// })
</script>