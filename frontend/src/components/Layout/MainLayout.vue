<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- 左侧菜单栏 - 固定宽度256px -->
    <div class="w-64 bg-white shadow-lg flex-shrink-0">
      <!-- Logo区域 -->
      <div class="flex items-center h-16 px-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">M</span>
          </div>
          <div>
            <h1 class="text-lg font-semibold text-gray-900">Mocker</h1>
            <p class="text-xs text-gray-500">API Platform</p>
          </div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="mt-6 px-3">
        <div class="space-y-1">
          <RouterLink
            to="/dashboard"
            :class="[
              'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Dashboard'
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
          >
            <svg class="mr-3 h-5 w-5" :class="$route.name === 'Dashboard' ? 'text-blue-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            仪表板
          </RouterLink>
          
          <RouterLink
            to="/mocks"
            :class="[
              'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'MockList'
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
          >
            <svg class="mr-3 h-5 w-5" :class="$route.name === 'MockList' ? 'text-blue-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
            </svg>
            Mock接口
          </RouterLink>
          
          <RouterLink
            to="/logs"
            :class="[
              'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'LogList'
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-500'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
          >
            <svg class="mr-3 h-5 w-5" :class="$route.name === 'LogList' ? 'text-blue-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            请求日志
          </RouterLink>
        </div>

      </nav>
    </div>

    <!-- 右侧主内容区 - 自动填充剩余空间 -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- 顶部导航栏 -->
      <header class="bg-white shadow-sm border-b border-gray-200 h-16 flex-shrink-0">
        <div class="h-full px-6 flex justify-between items-center">
          <!-- 面包屑导航 -->
          <nav class="flex" aria-label="Breadcrumb">
            <ol class="flex items-center space-x-2">
              <li>
                <RouterLink to="/dashboard" class="text-gray-400 hover:text-gray-500 text-sm font-medium">
                  首页
                </RouterLink>
              </li>
              <li v-if="$route.meta.title">
                <div class="flex items-center">
                  <svg class="h-4 w-4 text-gray-300 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                  <span class="text-gray-900 text-sm font-medium">
                    {{ $route.meta.title }}
                  </span>
                </div>
              </li>
            </ol>
          </nav>
          
          <!-- 右侧用户信息 -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">U</span>
              </div>
              <span class="text-sm font-medium text-gray-700">用户</span>
            </div>
          </div>
        </div>
      </header>
      
      <!-- 页面内容区 - 自动填充剩余空间 -->
      <main class="flex-1 p-6 overflow-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>
