<template>
  <div id="app">
    <RouterView />
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ToastContainer } from '@/components/Toast'
</script>

<style>
#app {
  min-height: 100vh;
}
</style>
