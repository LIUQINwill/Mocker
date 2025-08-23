<template>
  <div>
    <!-- 分类项 -->
    <div
      class="flex items-center justify-between py-2 px-4 hover:bg-gray-50 group"
      :style="{ paddingLeft: `${16 + level * 16}px` }"
    >
      <div class="flex items-center flex-1 min-w-0">
        <!-- 分类图标 -->
        <svg class="h-4 w-4 mr-2 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h2a2 2 0 012 2v0H8v0z"></path>
        </svg>

        <!-- 分类信息 -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center">
            <span class="text-sm font-medium text-gray-900 truncate">{{ category?.name || '未命名分类' }}</span>
            <span class="ml-2 text-xs text-gray-500">({{ category?.mock_count || 0 }})</span>
          </div>
          <div v-if="category?.description" class="text-xs text-gray-500 truncate">
            {{ category.description }}
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <button
          @click="$emit('edit', category)"
          class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded"
          title="编辑分类"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
          </svg>
        </button>
        
        <button
          @click="$emit('delete', category)"
          class="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded"
          title="删除分类"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- 子分类 -->
    <div v-if="category?.children && category.children.length > 0">
      <CategoryManageItem
        v-for="child in category.children"
        :key="child?.id || Math.random()"
        :category="child"
        :level="level + 1"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CategoryTree } from '@/types/category'

interface Props {
  category: CategoryTree
  level?: number
}

interface Emits {
  (e: 'edit', category: CategoryTree): void
  (e: 'delete', category: CategoryTree): void
}

withDefaults(defineProps<Props>(), {
  level: 0
})

defineEmits<Emits>()
</script>

<style scoped>
/* 样式通过 Tailwind 类实现 */
</style>