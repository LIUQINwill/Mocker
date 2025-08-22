<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- 左侧：移动端菜单按钮 + 面包屑 -->
        <div class="flex items-center">
          <!-- 移动端菜单按钮 -->
          <button
            @click="$emit('toggle-sidebar')"
            class="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <Bars3Icon class="h-6 w-6" />
          </button>
          
          <!-- 面包屑导航 -->
          <nav class="flex ml-4 lg:ml-0" aria-label="Breadcrumb">
            <ol class="flex items-center space-x-2">
              <li>
                <div class="flex items-center">
                  <RouterLink 
                    to="/dashboard" 
                    class="text-gray-400 hover:text-gray-500 text-sm font-medium"
                  >
                    首页
                  </RouterLink>
                </div>
              </li>
              <li v-if="currentRoute.meta.title">
                <div class="flex items-center">
                  <ChevronRightIcon class="h-4 w-4 text-gray-300 mx-2" />
                  <span class="text-gray-900 text-sm font-medium">
                    {{ currentRoute.meta.title }}
                  </span>
                </div>
              </li>
            </ol>
          </nav>
        </div>
        
        <!-- 右侧：搜索 + 用户菜单 -->
        <div class="flex items-center space-x-4">
          <!-- 全局搜索 -->
          <div class="hidden md:block">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon class="h-4 w-4 text-gray-400" />
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索Mock接口..."
                class="block w-64 pl-10 pr-3 py-2 border border-gray-300 rounded-lg text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                @keyup.enter="handleSearch"
              />
            </div>
          </div>
          
          <!-- 通知按钮 -->
          <button class="p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
            <BellIcon class="h-5 w-5" />
          </button>
          
          <!-- 用户菜单 -->
          <div class="relative">
            <button
              @click="userMenuOpen = !userMenuOpen"
              class="flex items-center space-x-2 p-2 text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">U</span>
              </div>
              <span class="hidden md:block text-sm font-medium">用户</span>
              <ChevronDownIcon class="h-4 w-4" />
            </button>
            
            <!-- 用户下拉菜单 -->
            <Transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-show="userMenuOpen"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
                @click.away="userMenuOpen = false"
              >
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  个人设置
                </a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  帮助文档
                </a>
                <div class="border-t border-gray-100"></div>
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  退出登录
                </a>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import {
  Bars3Icon,
  ChevronRightIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  BellIcon
} from '@heroicons/vue/24/outline'

// 定义事件
defineEmits<{
  'toggle-sidebar': []
}>()

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const userMenuOpen = ref(false)

const currentRoute = computed(() => route)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'MockList',
      query: { search: searchQuery.value.trim() }
    })
  }
}
</script>
