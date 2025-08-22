<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 侧边栏 -->
    <AppSidebar 
      :is-open="sidebarOpen" 
      @close="sidebarOpen = false" 
    />
    
    <!-- 主内容区 -->
    <div class="lg:pl-64">
      <!-- 顶部导航 -->
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <!-- 页面内容 -->
      <main class="py-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'

const sidebarOpen = ref(false)
</script>
