<template>
  <div class="category-tree">
    <!-- 头部 -->
    <div class="flex items-center justify-between p-3 border-b border-gray-200">
      <h3 class="text-sm font-medium text-gray-900">接口分类</h3>
      <button
        @click="$emit('manage-categories')"
        class="text-xs text-blue-600 hover:text-blue-800"
        title="管理分类"
      >
        管理
      </button>
    </div>

    <!-- 搜索框 -->
    <div class="p-3 border-b border-gray-200">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索分类..."
          class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
    </div>

    <!-- 分类树 -->
    <div class="flex-1 overflow-y-auto">
      <!-- 加载状态 -->
      <div v-if="loading" class="p-4 text-center text-sm text-gray-500">
        <svg class="animate-spin h-4 w-4 text-blue-500 mx-auto mb-2" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        正在加载...
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="p-4 text-center text-sm text-red-600">
        {{ error }}
      </div>

      <!-- 分类列表 -->
      <div v-else class="py-2">
        <!-- 全部接口 -->
        <div
          @click="selectCategory(null)"
          :class="[
            'flex items-center px-3 py-2 text-sm cursor-pointer hover:bg-gray-50',
            selectedCategoryId === null ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500' : 'text-gray-700'
          ]"
        >
          <svg class="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
          <span class="flex-1">全部接口</span>
          <span v-if="totalMockCount !== undefined" class="text-xs text-gray-500">{{ totalMockCount }}</span>
        </div>

        <!-- 未分类接口 -->
        <div
          @click="selectCategory(0)"
          :class="[
            'flex items-center px-3 py-2 text-sm cursor-pointer hover:bg-gray-50',
            selectedCategoryId === 0 ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500' : 'text-gray-700'
          ]"
        >
          <svg class="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span class="flex-1">未分类</span>
          <span v-if="uncategorizedCount !== undefined" class="text-xs text-gray-500">{{ uncategorizedCount }}</span>
        </div>

        <!-- 分类树节点 -->
        <CategoryTreeNode
          v-for="category in filteredCategoryTree"
          :key="category.id"
          :category="category"
          :selected-category-id="selectedCategoryId"
          :expanded-ids="expandedIds"
          @select-category="selectCategory"
          @toggle-expand="toggleExpand"
        />
      </div>
    </div>

    <!-- 统计信息 -->
    <div v-if="stats" class="p-3 border-t border-gray-200 text-xs text-gray-500">
      <div class="flex justify-between">
        <span>{{ stats.active_categories }} 个分类</span>
        <span>{{ stats.total_apis }} 个接口</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useCategories } from '@/composables/useCategories'
import CategoryTreeNode from './CategoryTreeNode.vue'
import type { CategoryTree } from '@/types/category'

interface Props {
  selectedCategoryId?: number | null
  totalMockCount?: number
  uncategorizedCount?: number
}

interface Emits {
  (e: 'select-category', categoryId: number | null): void
  (e: 'manage-categories'): void
}

const props = withDefaults(defineProps<Props>(), {
  selectedCategoryId: null
})

const emit = defineEmits<Emits>()

const {
  loading,
  error,
  categoryTree,
  stats,
  fetchCategoryTree,
  fetchCategoryStats
} = useCategories()

const searchQuery = ref('')
const expandedIds = ref<Set<number>>(new Set())

// 筛选后的分类树
const filteredCategoryTree = computed(() => {
  if (!searchQuery.value) {
    return categoryTree.value
  }

  const filterTree = (categories: CategoryTree[]): CategoryTree[] => {
    const filtered: CategoryTree[] = []
    
    for (const category of categories) {
      const nameMatch = category.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      const filteredChildren = filterTree(category.children || [])
      
      if (nameMatch || filteredChildren.length > 0) {
        filtered.push({
          ...category,
          children: filteredChildren
        })
        
        // 如果有匹配，自动展开
        if (nameMatch) {
          expandedIds.value.add(category.id)
        }
      }
    }
    
    return filtered
  }
  
  return filterTree(categoryTree.value)
})

// 选择分类
const selectCategory = (categoryId: number | null) => {
  emit('select-category', categoryId)
}

// 切换展开状态
const toggleExpand = (categoryId: number) => {
  if (expandedIds.value.has(categoryId)) {
    expandedIds.value.delete(categoryId)
  } else {
    expandedIds.value.add(categoryId)
  }
}

// 监听搜索变化，清空搜索时收起所有节点
watch(searchQuery, (newValue, oldValue) => {
  if (oldValue && !newValue) {
    expandedIds.value.clear()
  }
})

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([
    fetchCategoryTree(),
    fetchCategoryStats()
  ])
})

// 暴露刷新方法给父组件
defineExpose({
  refresh: async () => {
    await Promise.all([
      fetchCategoryTree(),
      fetchCategoryStats()
    ])
  }
})
</script>

<style scoped>
.category-tree {
  @apply h-full flex flex-col bg-white border-r border-gray-200;
}
</style>