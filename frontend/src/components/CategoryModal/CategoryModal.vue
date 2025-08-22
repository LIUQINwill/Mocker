<template>
  <div 
    v-if="visible" 
    class="fixed inset-0 z-50 overflow-y-auto" 
    @click.self="handleClose"
  >
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- 遮罩层 -->
      <div class="fixed inset-0 transition-opacity" @click="handleClose">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <!-- 弹窗内容 -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <!-- 头部 -->
        <div class="bg-white px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900">
              分类管理
            </h3>
            <button
              @click="handleClose"
              class="text-gray-400 hover:text-gray-600 focus:outline-none"
            >
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 主体内容 -->
        <div class="bg-gray-50 px-6 py-4 max-h-96 overflow-y-auto">
          <!-- 添加分类表单 -->
          <div class="bg-white rounded-lg p-4 mb-4 border border-gray-200">
            <h4 class="text-sm font-medium text-gray-900 mb-3">
              {{ editingCategory ? '编辑分类' : '添加分类' }}
            </h4>
            
            <form @submit.prevent="handleSubmit" class="space-y-3">
              <!-- 分类名称 -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">分类名称 *</label>
                <input
                  v-model="form.name"
                  type="text"
                  required
                  maxlength="50"
                  placeholder="请输入分类名称"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <!-- 分类描述 -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">分类描述</label>
                <textarea
                  v-model="form.description"
                  rows="2"
                  maxlength="200"
                  placeholder="请输入分类描述（可选）"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                ></textarea>
              </div>

              <!-- 父分类选择 -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">父分类</label>
                <select
                  v-model="form.parent_id"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option :value="null">根分类</option>
                  <option
                    v-for="category in selectableCategories"
                    :key="category.id"
                    :value="category.id"
                    :disabled="category.id === editingCategory?.id"
                  >
                    {{ '　'.repeat(category.level) }}{{ category.name }}
                  </option>
                </select>
              </div>

              <!-- 操作按钮 -->
              <div class="flex justify-end space-x-3 pt-2">
                <button
                  v-if="editingCategory"
                  @click="cancelEdit"
                  type="button"
                  class="px-3 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  取消
                </button>
                <button
                  type="submit"
                  :disabled="loading || !form.name.trim()"
                  class="px-3 py-2 text-xs font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ editingCategory ? '更新' : '添加' }}
                </button>
              </div>
            </form>
          </div>

          <!-- 分类列表 -->
          <div class="bg-white rounded-lg border border-gray-200">
            <div class="px-4 py-3 border-b border-gray-200">
              <h4 class="text-sm font-medium text-gray-900">现有分类</h4>
            </div>

            <!-- 分类树 -->
            <div class="max-h-64 overflow-y-auto">
              <div v-if="categoryLoading" class="p-4 text-center text-sm text-gray-500">
                正在加载分类...
              </div>
              
              <div v-else-if="categoryError" class="p-4 text-center text-sm text-red-600">
                {{ categoryError }}
              </div>
              
              <div v-else-if="categoryTree.length === 0" class="p-4 text-center text-sm text-gray-500">
                暂无分类，请先添加分类
              </div>
              
              <div v-else class="py-2">
                <CategoryManageItem
                  v-for="category in categoryTree"
                  :key="category.id"
                  :category="category"
                  :level="0"
                  @edit="startEdit"
                  @delete="handleDelete"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 底部 -->
        <div class="bg-gray-50 px-6 py-3 border-t border-gray-200">
          <div class="flex justify-between items-center">
            <div class="text-xs text-gray-500">
              提示：删除分类前，请确保该分类下没有接口或子分类
            </div>
            <button
              @click="handleClose"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              完成
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
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

const {
  loading,
  error: categoryError,
  categoryTree,
  flattenedCategories,
  fetchCategoryTree,
  createCategory,
  updateCategory,
  deleteCategory,
  loading: categoryLoading
} = useCategories()

// 表单数据
const form = ref<CategoryCreate>({
  name: '',
  description: '',
  parent_id: null,
  sort_order: 0,
  is_active: true
})

// 编辑状态
const editingCategory = ref<CategoryTree | null>(null)

// 可选择的父分类（排除自己和其子分类）
const selectableCategories = computed(() => {
  if (!editingCategory.value) {
    return flattenedCategories.value
  }

  // 递归获取所有子分类ID
  const getDescendantIds = (category: CategoryTree): number[] => {
    const ids = [category.id]
    if (category.children) {
      for (const child of category.children) {
        ids.push(...getDescendantIds(child))
      }
    }
    return ids
  }

  const excludeIds = getDescendantIds(editingCategory.value)
  return flattenedCategories.value.filter(cat => !excludeIds.includes(cat.id))
})

// 处理提交
const handleSubmit = async () => {
  if (!form.value.name.trim()) return

  let success = false
  
  if (editingCategory.value) {
    // 更新分类
    const updateData: CategoryUpdate = {
      name: form.value.name.trim(),
      description: form.value.description?.trim() || '',
      parent_id: form.value.parent_id,
      sort_order: form.value.sort_order,
      is_active: form.value.is_active
    }
    
    const result = await updateCategory(editingCategory.value.id, updateData)
    success = !!result
  } else {
    // 创建分类
    const result = await createCategory({
      ...form.value,
      name: form.value.name.trim(),
      description: form.value.description?.trim() || ''
    })
    success = !!result
  }

  if (success) {
    resetForm()
    emit('updated')
  }
}

// 开始编辑
const startEdit = (category: CategoryTree) => {
  editingCategory.value = category
  form.value = {
    name: category.name,
    description: category.description || '',
    parent_id: category.parent_id,
    sort_order: category.sort_order,
    is_active: category.is_active
  }
}

// 取消编辑
const cancelEdit = () => {
  editingCategory.value = null
  resetForm()
}

// 重置表单
const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    parent_id: null,
    sort_order: 0,
    is_active: true
  }
  editingCategory.value = null
}

// 处理删除
const handleDelete = async (category: CategoryTree) => {
  if (!confirm(`确定要删除分类"${category.name}"吗？\n注意：如果该分类下有接口或子分类，删除将失败。`)) {
    return
  }

  const success = await deleteCategory(category.id)
  if (success) {
    emit('updated')
    // 如果正在编辑被删除的分类，取消编辑
    if (editingCategory.value?.id === category.id) {
      cancelEdit()
    }
  }
}

// 处理关闭
const handleClose = () => {
  resetForm()
  emit('close')
}

// 监听弹窗显示状态
watch(() => props.visible, async (visible) => {
  if (visible) {
    await fetchCategoryTree()
    await nextTick()
    // 重置表单和编辑状态
    resetForm()
  }
})
</script>

<style scoped>
/* 动画样式通过 Tailwind 类实现 */
</style>