<template>
  <!-- 移动端遮罩 -->
  <div 
    v-show="isOpen" 
    class="fixed inset-0 z-40 lg:hidden"
    @click="$emit('close')"
  >
    <div class="fixed inset-0 bg-gray-600 bg-opacity-75"></div>
  </div>

  <!-- 侧边栏 -->
  <div 
    :class="[
      'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
      isOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <!-- Logo区域 -->
    <div class="flex items-center justify-between h-16 px-6 border-b border-gray-200">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-sm">M</span>
        </div>
        <div>
          <h1 class="text-lg font-semibold text-gray-900">Mocker</h1>
          <p class="text-xs text-gray-500">API Platform</p>
        </div>
      </div>
      
      <!-- 移动端关闭按钮 -->
      <button
        @click="$emit('close')"
        class="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
      >
        <XMarkIcon class="h-5 w-5" />
      </button>
    </div>

    <!-- 导航菜单 -->
    <nav class="mt-6 px-3">
      <div class="space-y-1">
        <RouterLink
          v-for="item in navigation"
          :key="item.name"
          :to="item.to"
          :class="[
            'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
            $route.name === item.name
              ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-500'
              : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
          ]"
        >
          <component 
            :is="item.icon" 
            :class="[
              'mr-3 h-5 w-5 transition-colors',
              $route.name === item.name
                ? 'text-primary-500'
                : 'text-gray-400 group-hover:text-gray-500'
            ]"
          />
          {{ item.label }}
        </RouterLink>
      </div>

    </nav>

    <!-- 底部信息 -->
    <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
      <div class="text-xs text-gray-500 text-center">
        <p>Version 0.1.0</p>
        <p class="mt-1">© 2024 Mocker Platform</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import {
  ChartBarIcon,
  CodeBracketIcon,
  DocumentTextIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// 定义props和events
defineProps<{
  isOpen: boolean
}>()

defineEmits<{
  close: []
}>()

const route = useRoute()

// 导航菜单配置
const navigation = [
  {
    name: 'Dashboard',
    label: '仪表板',
    to: '/dashboard',
    icon: ChartBarIcon
  },
  {
    name: 'MockList',
    label: 'Mock接口',
    to: '/mocks',
    icon: CodeBracketIcon
  },
  {
    name: 'LogList',
    label: '请求日志',
    to: '/logs',
    icon: DocumentTextIcon
  }
]
</script>
