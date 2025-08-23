<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 space-y-3 pointer-events-none">
      <Toast
        v-for="toastItem in toasts"
        :key="toastItem.id"
        :visible="true"
        :type="toastItem.type"
        :title="toastItem.title"
        :message="toastItem.message"
        :duration="toastItem.duration"
        @close="removeToast(toastItem.id)"
        class="pointer-events-auto"
      />
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { toast } from '@/composables/useToast'
import { Toast } from '@/components/Toast'

const { toasts, removeToast } = toast
</script>