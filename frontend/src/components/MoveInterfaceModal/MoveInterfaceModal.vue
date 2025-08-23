<template>
  <div
    v-if="visible"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="handleCancel"
  >
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
      <!-- 弹窗头部 -->
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">
            {{ isBatch ? `移动${selectedMocks.length}个接口` : '移动接口' }}
          </h3>
          <button
            @click="handleCancel"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- 弹窗内容 -->
      <div class="px-6 py-4">
        <div class="space-y-4">
          <!-- 当前接口信息 -->
          <div v-if="!isBatch && selectedMocks.length === 1" class="bg-gray-50 p-3 rounded-md">
            <div class="text-sm text-gray-600 mb-1">当前接口：</div>
            <div class="font-medium text-gray-900">{{ selectedMocks[0].name }}</div>
            <div class="text-sm text-gray-500">{{ selectedMocks[0].method }} {{ selectedMocks[0].path }}</div>
          </div>

          <!-- 批量移动信息 -->
          <div v-if="isBatch" class="bg-gray-50 p-3 rounded-md">
            <div class="text-sm text-gray-600 mb-2">选中的接口：</div>
            <div class="max-h-32 overflow-y-auto space-y-1">
              <div
                v-for="mock in selectedMocks"
                :key="mock.id"
                class="text-sm text-gray-900"
              >
                {{ mock.name }} ({{ mock.method }} {{ mock.path }})
              </div>
            </div>
          </div>

          <!-- 分类选择 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              选择目标分类：
            </label>
            <select
              v-model="selectedCategoryId"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">选择分类</option>
              <option value="0">未分类</option>
              <option
                v-for="category in availableCategories"
                :key="category.id"
                :value="category.id"
              >
                {{ '　'.repeat(category.level) }}{{ category.name }}
              </option>
            </select>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="text-red-600 text-sm">
            {{ errorMessage }}
          </div>
        </div>
      </div>

      <!-- 弹窗底部 -->
      <div class="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
        <button
          @click="handleCancel"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          取消
        </button>
        <button
          @click="handleConfirm"
          :disabled="!selectedCategoryId && selectedCategoryId !== 0"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="inline-block animate-spin w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full"></span>
          确认移动
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useCategories } from '@/composables/useCategories'
import { categoryApi } from '@/api/categories'
import { useToast } from '@/composables/useToast'
import type { MockAPI } from '@/types/mock'
import type { Category } from '@/types/category'

// Props
interface Props {
  visible: boolean
  selectedMocks: MockAPI[]
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  close: []
  moved: []
}>()

// 组合函数
const { flattenedCategories, fetchCategoryTree } = useCategories()
const toast = useToast()

// 状态
const selectedCategoryId = ref<number | string>('')
const loading = ref(false)
const errorMessage = ref('')

// 计算属性
const isBatch = computed(() => props.selectedMocks.length > 1)
const availableCategories = computed(() => flattenedCategories.value || [])

// 处理取消
const handleCancel = () => {
  selectedCategoryId.value = ''
  errorMessage.value = ''
  emit('close')
}

// 处理确认移动
const handleConfirm = async () => {
  if (!selectedCategoryId.value && selectedCategoryId.value !== 0) {
    errorMessage.value = '请选择目标分类'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const mockIds = props.selectedMocks.map(mock => mock.id)
    
    // 处理分类ID：0表示未分类，应该传null给后端
    let categoryId: number | null
    if (selectedCategoryId.value === 0 || selectedCategoryId.value === '0') {
      categoryId = null
    } else {
      categoryId = Number(selectedCategoryId.value)
    }
    
    console.log('准备发送的数据:', {
      category_id: categoryId,
      mock_ids: mockIds
    })
    
    await categoryApi.batchUpdateMockCategory({
      category_id: categoryId,
      mock_ids: mockIds
    })

    const targetCategoryName = categoryId === null ? '未分类' : 
      availableCategories.value.find(c => c.id === categoryId)?.name || '未知分类'

    toast.success('移动成功', `已将 ${props.selectedMocks.length} 个接口移动到"${targetCategoryName}"`)

    emit('moved')
    handleCancel()
  } catch (error: any) {
    console.error('移动接口失败:', error)
    errorMessage.value = error.message || '移动接口失败，请重试'
    toast.error('移动失败', errorMessage.value)
  } finally {
    loading.value = false
  }
}

// 监听弹窗显示状态，显示时获取分类数据
watch(() => props.visible, async (visible) => {
  if (visible) {
    try {
      await fetchCategoryTree()
    } catch (error) {
      console.error('获取分类数据失败:', error)
    }
  }
})

// 组件挂载时获取分类数据
onMounted(async () => {
  if (props.visible) {
    try {
      await fetchCategoryTree()
    } catch (error) {
      console.error('获取分类数据失败:', error)
    }
  }
})
</script>