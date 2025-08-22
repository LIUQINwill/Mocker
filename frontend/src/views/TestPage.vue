<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">
          🎭 Mocker Platform
        </h1>
        <p class="text-gray-600 mb-6">
          前端页面加载成功！
        </p>
        <div class="space-y-4">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-green-800">
                  Vue 3 + TypeScript 正常运行
                </p>
              </div>
            </div>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-blue-800">
                  Tailwind CSS 样式正常
                </p>
              </div>
            </div>
          </div>
          
          <button 
            @click="testClick"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
          >
            测试点击事件
          </button>
          
          <p v-if="clicked" class="text-green-600 text-sm">
            ✅ 点击事件正常工作！
          </p>
        </div>
        
        <div class="mt-8 text-sm text-gray-500">
          <p>当前时间: {{ currentTime }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const clicked = ref(false)
const currentTime = ref('')

const testClick = () => {
  clicked.value = true
  setTimeout(() => {
    clicked.value = false
  }, 2000)
}

const updateTime = () => {
  currentTime.value = new Date().toLocaleString('zh-CN')
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
})
</script>
