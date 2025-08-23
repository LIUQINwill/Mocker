/**
 * Toast通知管理组合式函数
 */
import { ref, reactive } from 'vue'

export interface ToastItem {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

const toasts = ref<ToastItem[]>([])
let toastId = 0

export function useToast() {
  /**
   * 添加Toast通知
   */
  const addToast = (toast: Omit<ToastItem, 'id'>) => {
    const id = `toast-${++toastId}`
    const newToast: ToastItem = {
      id,
      duration: 5000,
      ...toast
    }
    
    toasts.value.push(newToast)
    
    // 如果设置了持续时间，自动移除
    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, newToast.duration)
    }
    
    return id
  }

  /**
   * 移除Toast通知
   */
  const removeToast = (id: string) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  /**
   * 清空所有Toast通知
   */
  const clearToasts = () => {
    toasts.value = []
  }

  /**
   * 显示成功通知
   */
  const success = (title: string, message?: string, duration?: number) => {
    return addToast({
      type: 'success',
      title,
      message,
      duration
    })
  }

  /**
   * 显示错误通知
   */
  const error = (title: string, message?: string, duration?: number) => {
    return addToast({
      type: 'error',
      title,
      message,
      duration: duration || 0 // 错误默认不自动关闭
    })
  }

  /**
   * 显示警告通知
   */
  const warning = (title: string, message?: string, duration?: number) => {
    return addToast({
      type: 'warning',
      title,
      message,
      duration
    })
  }

  /**
   * 显示信息通知
   */
  const info = (title: string, message?: string, duration?: number) => {
    return addToast({
      type: 'info',
      title,
      message,
      duration
    })
  }

  return {
    toasts,
    addToast,
    removeToast,
    clearToasts,
    success,
    error,
    warning,
    info
  }
}

// 创建全局实例
export const toast = useToast()