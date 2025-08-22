<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- 测试标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          🎭 Mocker Platform
        </h1>
        <p class="text-xl text-gray-600">
          Mock API 管理平台 - 样式测试页面
        </p>
      </div>

      <!-- 测试卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- 卡片1 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">快速创建</h3>
              <p class="text-sm text-gray-500">轻松创建Mock接口</p>
            </div>
          </div>
          <p class="text-gray-600">
            通过简单的表单配置，快速创建Mock API接口，支持多种HTTP方法和自定义响应。
          </p>
        </div>

        <!-- 卡片2 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">实时监控</h3>
              <p class="text-sm text-gray-500">监控API调用情况</p>
            </div>
          </div>
          <p class="text-gray-600">
            实时查看Mock接口的调用情况，包括请求次数、响应时间和成功率等关键指标。
          </p>
        </div>

        <!-- 卡片3 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">灵活配置</h3>
              <p class="text-sm text-gray-500">自定义响应内容</p>
            </div>
          </div>
          <p class="text-gray-600">
            支持自定义响应状态码、响应头和响应体，满足各种测试场景的需求。
          </p>
        </div>
      </div>

      <!-- 按钮测试 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">按钮样式测试</h3>
        <div class="flex flex-wrap gap-4">
          <button class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
            主要按钮
          </button>
          <button class="px-4 py-2 bg-gray-200 text-gray-900 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            次要按钮
          </button>
          <button class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">
            成功按钮
          </button>
          <button class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2">
            危险按钮
          </button>
        </div>
      </div>

      <!-- 表单测试 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">表单样式测试</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">输入框</label>
            <input 
              type="text" 
              placeholder="请输入内容..."
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">选择框</label>
            <select class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              <option>选项1</option>
              <option>选项2</option>
              <option>选项3</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 状态指示器测试 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">状态指示器测试</h3>
        <div class="space-y-3">
          <div class="flex items-center">
            <div class="w-3 h-3 bg-green-400 rounded-full mr-3"></div>
            <span class="text-green-700">运行中</span>
          </div>
          <div class="flex items-center">
            <div class="w-3 h-3 bg-yellow-400 rounded-full mr-3"></div>
            <span class="text-yellow-700">警告</span>
          </div>
          <div class="flex items-center">
            <div class="w-3 h-3 bg-red-400 rounded-full mr-3"></div>
            <span class="text-red-700">错误</span>
          </div>
          <div class="flex items-center">
            <div class="w-3 h-3 bg-gray-400 rounded-full mr-3"></div>
            <span class="text-gray-700">停止</span>
          </div>
        </div>
      </div>

      <!-- 导航测试 -->
      <div class="mt-8 text-center">
        <div class="space-x-4">
          <RouterLink 
            to="/dashboard" 
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            返回仪表板
          </RouterLink>
          <RouterLink 
            to="/mocks" 
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Mock接口管理
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
