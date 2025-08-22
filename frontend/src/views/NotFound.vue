<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <!-- 404图标 -->
        <div class="mx-auto h-24 w-24 text-gray-400 mb-6">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.5-.935-6.072-2.456M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
          </svg>
        </div>
        
        <!-- 404标题 -->
        <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">页面未找到</h2>
        <p class="text-gray-500 mb-8">
          抱歉，您访问的页面不存在或已被移动。
        </p>
        
        <!-- 操作按钮 -->
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <RouterLink
            to="/dashboard"
            class="btn btn-primary"
          >
            <HomeIcon class="h-4 w-4 mr-2" />
            返回首页
          </RouterLink>
          
          <button
            @click="goBack"
            class="btn btn-secondary"
          >
            <ArrowLeftIcon class="h-4 w-4 mr-2" />
            返回上页
          </button>
        </div>
        
        <!-- 快速链接 -->
        <div class="mt-12">
          <h3 class="text-sm font-medium text-gray-900 mb-4">您可能想要访问：</h3>
          <div class="space-y-2">
            <RouterLink
              to="/mocks"
              class="block text-primary-600 hover:text-primary-500 text-sm"
            >
              Mock接口管理
            </RouterLink>
            <RouterLink
              to="/logs"
              class="block text-primary-600 hover:text-primary-500 text-sm"
            >
              请求日志
            </RouterLink>
            <RouterLink
              to="/mocks/create"
              class="block text-primary-600 hover:text-primary-500 text-sm"
            >
              创建Mock接口
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { HomeIcon, ArrowLeftIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>
