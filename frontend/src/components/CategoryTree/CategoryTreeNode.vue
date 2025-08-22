<template>
  <div>
    <!-- 分类节点 -->
    <div
      @click="handleSelectCategory"
      :class="[
        'flex items-center py-1 px-3 text-sm cursor-pointer hover:bg-gray-50 group',
        { 'bg-blue-50 text-blue-700 border-r-2 border-blue-500': isSelected },
        { 'text-gray-700': !isSelected }
      ]"
      :style="{ paddingLeft: `${12 + level * 16}px` }"
    >
      <!-- 展开/收起按钮 -->
      <button
        v-if="hasChildren"
        @click.stop="handleToggleExpand"
        class="mr-1 p-0.5 hover:bg-gray-200 rounded"
        :class="{ 'text-blue-600': isSelected }"
      >
        <svg
          class="h-3 w-3 transition-transform duration-200"
          :class="{ 'rotate-90': isExpanded }"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </button>
      
      <!-- 占位符（无子分类时） -->
      <div v-else class="w-4 mr-1"></div>

      <!-- 分类图标 -->
      <svg class="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h2a2 2 0 012 2v0H8v0z"></path>
      </svg>

      <!-- 分类名称 -->
      <span class="flex-1 truncate" :title="category.name">{{ category.name }}</span>

      <!-- 接口数量 -->
      <span 
        v-if="category.mock_count > 0" 
        class="text-xs text-gray-500 ml-1"
        :class="{ 'text-blue-500': isSelected }"
      >
        {{ category.mock_count }}
      </span>

      <!-- 操作按钮（悬停时显示） -->
      <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-200 ml-2">
        <button
          @click.stop="$emit('edit-category', category)"
          class="p-1 hover:bg-gray-200 rounded text-gray-400 hover:text-gray-600"
          title="编辑分类"
        >
          <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- 子分类 -->
    <div v-if="hasChildren && isExpanded">
      <CategoryTreeNode
        v-for="child in category.children"
        :key="child.id"
        :category="child"
        :level="level + 1"
        :selected-category-id="selectedCategoryId"
        :expanded-ids="expandedIds"
        @select-category="$emit('select-category', $event)"
        @toggle-expand="$emit('toggle-expand', $event)"
        @edit-category="$emit('edit-category', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { CategoryTree } from '@/types/category'

interface Props {
  category: CategoryTree
  level?: number
  selectedCategoryId?: number | null
  expandedIds?: Set<number>
}

interface Emits {
  (e: 'select-category', categoryId: number): void
  (e: 'toggle-expand', categoryId: number): void
  (e: 'edit-category', category: CategoryTree): void
}

const props = withDefaults(defineProps<Props>(), {
  level: 0,
  selectedCategoryId: null,
  expandedIds: () => new Set()
})

const emit = defineEmits<Emits>()

// 计算属性
const hasChildren = computed(() => {
  return props.category.children && props.category.children.length > 0
})

const isExpanded = computed(() => {
  return props.expandedIds?.has(props.category.id) || false
})

const isSelected = computed(() => {
  return props.selectedCategoryId === props.category.id
})

// 事件处理
const handleSelectCategory = () => {
  emit('select-category', props.category.id)
}

const handleToggleExpand = () => {
  emit('toggle-expand', props.category.id)
}
</script>

<style scoped>
/* 动画样式已通过 Tailwind 类实现 */
</style>