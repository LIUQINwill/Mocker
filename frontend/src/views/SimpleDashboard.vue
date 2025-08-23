<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          仪表板
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          欢迎使用Mocker API平台，这里是您的Mock接口管理中心
        </p>
      </div>
      <div class="mt-4 flex md:mt-0 md:ml-4">
        <RouterLink
          to="/mocks/create"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          创建Mock接口
        </RouterLink>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <!-- 总接口数 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  总接口数
                </dt>
                <dd class="text-2xl font-semibold text-gray-900">
                  <span v-if="loading">--</span>
                  <span v-else>{{ stats.total_mocks }}</span>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- 今日请求数 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  今日请求数
                </dt>
                <dd class="text-2xl font-semibold text-gray-900">
                  <span v-if="loading">--</span>
                  <span v-else>{{ stats.today_requests }}</span>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- 成功率 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  成功率
                </dt>
                <dd class="text-2xl font-semibold text-gray-900">
                  <span v-if="loading">--</span>
                  <span v-else>{{ stats.success_rate }}%</span>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- 平均响应时间 -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  平均响应时间
                </dt>
                <dd class="text-2xl font-semibold text-gray-900">
                  <span v-if="loading">--</span>
                  <span v-else>{{ stats.avg_response_time }}ms</span>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近的Mock接口 -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
          最近的Mock接口
        </h3>
        <div v-if="loading" class="space-y-3">
          <div class="animate-pulse">
            <div class="flex space-x-4">
              <div class="rounded-full bg-gray-300 h-10 w-10"></div>
              <div class="flex-1 space-y-2 py-1">
                <div class="h-4 bg-gray-300 rounded w-3/4"></div>
                <div class="h-4 bg-gray-300 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="recentMocks.length === 0" class="text-center py-8">
          <div class="text-gray-400 mb-2">
            <svg class="h-12 w-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
            </svg>
          </div>
          <p class="text-gray-500">暂无Mock接口</p>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="mock in recentMocks" 
            :key="mock.id"
            class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div class="flex items-center space-x-3">
              <span 
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  getMethodBadgeClass(mock.method)
                ]"
              >
                {{ mock.method }}
              </span>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ mock.name }}</p>
                <p class="text-sm text-gray-500">{{ mock.path }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <div 
                :class="[
                  'w-2 h-2 rounded-full',
                  mock.is_active ? 'bg-green-400' : 'bg-gray-400'
                ]"
              ></div>
              <span 
                :class="[
                  'text-sm',
                  mock.is_active ? 'text-green-700' : 'text-gray-500'
                ]"
              >
                {{ mock.is_active ? '已启用' : '已禁用' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速导航 -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
          快速操作
        </h3>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <RouterLink
            to="/mocks"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 ring-4 ring-white">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                </svg>
              </span>
            </div>
            <div class="mt-8">
              <h3 class="text-lg font-medium">
                <span class="absolute inset-0" aria-hidden="true"></span>
                管理Mock接口
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                查看、编辑和管理所有Mock接口
              </p>
            </div>
          </RouterLink>

          <RouterLink
            to="/logs"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-green-50 text-green-700 ring-4 ring-white">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </span>
            </div>
            <div class="mt-8">
              <h3 class="text-lg font-medium">
                <span class="absolute inset-0" aria-hidden="true"></span>
                查看请求日志
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                分析和监控API请求记录
              </p>
            </div>
          </RouterLink>

          <RouterLink
            to="/mocks/create"
            class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div>
              <span class="rounded-lg inline-flex p-3 bg-purple-50 text-purple-700 ring-4 ring-white">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
              </span>
            </div>
            <div class="mt-8">
              <h3 class="text-lg font-medium">
                <span class="absolute inset-0" aria-hidden="true"></span>
                创建新接口
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                快速创建新的Mock API接口
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- 系统状态 -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
          系统状态
        </h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500">前端服务</span>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <span class="w-2 h-2 bg-green-400 rounded-full mr-1"></span>
              运行中
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500">后端API</span>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <span class="w-2 h-2 bg-green-400 rounded-full mr-1"></span>
              运行中
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500">数据库连接</span>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <span class="w-2 h-2 bg-green-400 rounded-full mr-1"></span>
              正常
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

// 统计数据状态
const loading = ref(true)
const stats = ref({
  total_mocks: 0,
  active_mocks: 0,
  today_requests: 0,
  success_rate: 0.0,
  avg_response_time: 0.0
})

// 最近的Mock接口数据
const recentMocks = ref([])

// 获取方法标签样式
const getMethodBadgeClass = (method: string) => {
  const methodClasses = {
    'GET': 'bg-green-100 text-green-800',
    'POST': 'bg-blue-100 text-blue-800',
    'PUT': 'bg-yellow-100 text-yellow-800',
    'DELETE': 'bg-red-100 text-red-800',
    'PATCH': 'bg-purple-100 text-purple-800'
  }
  return methodClasses[method] || 'bg-gray-100 text-gray-800'
}

// 获取仪表板统计数据
const fetchDashboardStats = async () => {
  try {
    const response = await fetch('/api/v1/dashboard/stats')
    if (!response.ok) {
      throw new Error(`HTTP错误! 状态: ${response.status}`)
    }
    const data = await response.json()
    
    stats.value = data.stats
    recentMocks.value = data.recent_mocks
    loading.value = false
  } catch (error) {
    console.error('获取仪表板数据失败:', error)
    // 如果API请求失败，显示默认数据
    stats.value = {
      total_mocks: 0,
      active_mocks: 0,
      today_requests: 0,
      success_rate: 0.0,
      avg_response_time: 0.0
    }
    recentMocks.value = []
    loading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDashboardStats()
})
</script>
