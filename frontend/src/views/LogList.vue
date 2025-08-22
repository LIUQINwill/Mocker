<template>
  <div class="space-y-6">
    <!-- 页面标题和操作 -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          请求日志
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          查看和分析Mock接口的请求记录
        </p>
      </div>
      <div class="mt-4 flex space-x-3 md:mt-0 md:ml-4">
        <button
          @click="refreshData"
          :disabled="loading"
          class="btn btn-secondary"
        >
          <ArrowPathIcon class="h-4 w-4 mr-2" />
          刷新
        </button>
        <button
          @click="clearLogsConfirm"
          class="btn btn-danger"
        >
          <TrashIcon class="h-4 w-4 mr-2" />
          清空日志
        </button>
      </div>
    </div>

    <!-- 筛选器 -->
    <div class="card">
      <div class="card-body">
        <div class="grid grid-cols-1 gap-4 md:grid-cols-5">
          <!-- 方法筛选 -->
          <div>
            <label class="form-label">HTTP方法</label>
            <select v-model="selectedMethod" class="form-select" @change="handleFilter">
              <option value="">全部方法</option>
              <option value="GET">GET</option>
              <option value="POST">POST</option>
              <option value="PUT">PUT</option>
              <option value="DELETE">DELETE</option>
              <option value="PATCH">PATCH</option>
            </select>
          </div>

          <!-- 状态码筛选 -->
          <div>
            <label class="form-label">状态码</label>
            <select v-model="selectedStatus" class="form-select" @change="handleFilter">
              <option value="">全部状态</option>
              <option value="200">200 - 成功</option>
              <option value="201">201 - 已创建</option>
              <option value="400">400 - 请求错误</option>
              <option value="404">404 - 未找到</option>
              <option value="500">500 - 服务器错误</option>
            </select>
          </div>

          <!-- 开始日期 -->
          <div>
            <label class="form-label">开始日期</label>
            <input
              v-model="startDate"
              type="date"
              class="form-input"
              @change="handleFilter"
            />
          </div>

          <!-- 结束日期 -->
          <div>
            <label class="form-label">结束日期</label>
            <input
              v-model="endDate"
              type="date"
              class="form-input"
              @change="handleFilter"
            />
          </div>

          <!-- 重置按钮 -->
          <div class="flex items-end">
            <button
              @click="resetFilters"
              class="btn btn-secondary w-full"
            >
              重置筛选
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 日志列表 -->
    <div class="card">
      <div class="card-header">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">
            请求记录 ({{ pagination.total }})
          </h3>
          <div class="flex items-center space-x-2 text-sm text-gray-500">
            <span>每页显示</span>
            <select 
              v-model="pagination.size" 
              class="form-select text-sm py-1"
              @change="handlePageSizeChange"
            >
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
            </select>
            <span>条</span>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="card-body">
        <div class="flex items-center justify-center py-12">
          <div class="loading-spinner w-8 h-8"></div>
          <span class="ml-2 text-gray-500">加载中...</span>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="logs.length === 0" class="card-body">
        <div class="text-center py-12">
          <DocumentTextIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">暂无请求记录</h3>
          <p class="text-gray-500">当有Mock接口被调用时，请求记录会显示在这里</p>
        </div>
      </div>

      <!-- 日志列表 -->
      <div v-else class="card-body p-0">
        <div class="space-y-1">
          <div 
            v-for="log in logs" 
            :key="log.id"
            class="border-b border-gray-100 last:border-b-0"
          >
            <!-- 日志摘要 -->
            <div 
              @click="toggleLogDetail(log.id)"
              class="flex items-center justify-between p-4 hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <div class="flex items-center space-x-4 flex-1">
                <!-- 状态指示器 -->
                <div 
                  :class="[
                    'w-3 h-3 rounded-full flex-shrink-0',
                    getStatusColor(log.response_status_code)
                  ]"
                ></div>

                <!-- 请求信息 -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-3">
                    <span 
                      :class="[
                        'badge',
                        log.request_method === 'GET' ? 'badge-success' :
                        log.request_method === 'POST' ? 'badge-info' :
                        log.request_method === 'PUT' ? 'badge-warning' :
                        log.request_method === 'DELETE' ? 'badge-danger' :
                        'badge-gray'
                      ]"
                    >
                      {{ log.request_method }}
                    </span>
                    <span class="font-medium text-gray-900 truncate">
                      {{ log.request_path }}
                    </span>
                    <span 
                      :class="[
                        'text-sm',
                        log.response_status_code >= 200 && log.response_status_code < 300 ? 'text-green-600' :
                        log.response_status_code >= 400 ? 'text-red-600' :
                        'text-yellow-600'
                      ]"
                    >
                      {{ log.response_status_code }}
                    </span>
                  </div>
                  <div class="flex items-center space-x-4 mt-1 text-sm text-gray-500">
                    <span>{{ formatTime(log.created_at) }}</span>
                    <span v-if="log.response_time_ms">{{ log.response_time_ms }}ms</span>
                    <span v-if="log.client_ip">{{ log.client_ip }}</span>
                  </div>
                </div>

                <!-- 展开图标 -->
                <div class="flex-shrink-0">
                  <ChevronDownIcon 
                    :class="[
                      'h-5 w-5 text-gray-400 transition-transform',
                      expandedLogs.has(log.id) ? 'transform rotate-180' : ''
                    ]"
                  />
                </div>
              </div>
            </div>

            <!-- 日志详情 -->
            <div 
              v-show="expandedLogs.has(log.id)"
              class="px-4 pb-4 bg-gray-50 border-t border-gray-200"
            >
              <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
                <!-- 请求详情 -->
                <div>
                  <h4 class="text-sm font-medium text-gray-900 mb-2">请求信息</h4>
                  <div class="space-y-2 text-sm">
                    <div>
                      <span class="text-gray-500">路径:</span>
                      <code class="ml-2 bg-white px-2 py-1 rounded">{{ log.request_path }}</code>
                    </div>
                    <div>
                      <span class="text-gray-500">方法:</span>
                      <span class="ml-2">{{ log.request_method }}</span>
                    </div>
                    <div v-if="log.request_headers">
                      <span class="text-gray-500">请求头:</span>
                      <pre class="mt-1 bg-white p-2 rounded text-xs overflow-x-auto">{{ formatJson(log.request_headers) }}</pre>
                    </div>
                    <div v-if="log.request_body">
                      <span class="text-gray-500">请求体:</span>
                      <pre class="mt-1 bg-white p-2 rounded text-xs overflow-x-auto">{{ formatJson(log.request_body) }}</pre>
                    </div>
                  </div>
                </div>

                <!-- 响应详情 -->
                <div>
                  <h4 class="text-sm font-medium text-gray-900 mb-2">响应信息</h4>
                  <div class="space-y-2 text-sm">
                    <div>
                      <span class="text-gray-500">状态码:</span>
                      <span class="ml-2">{{ log.response_status_code }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">响应时间:</span>
                      <span class="ml-2">{{ log.response_time_ms }}ms</span>
                    </div>
                    <div v-if="log.response_headers">
                      <span class="text-gray-500">响应头:</span>
                      <pre class="mt-1 bg-white p-2 rounded text-xs overflow-x-auto">{{ formatJson(log.response_headers) }}</pre>
                    </div>
                    <div v-if="log.response_body">
                      <span class="text-gray-500">响应体:</span>
                      <pre class="mt-1 bg-white p-2 rounded text-xs overflow-x-auto">{{ formatJson(log.response_body) }}</pre>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="pagination.pages > 1" class="card-footer">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-500">
            显示第 {{ (pagination.page - 1) * pagination.size + 1 }} - 
            {{ Math.min(pagination.page * pagination.size, pagination.total) }} 条，
            共 {{ pagination.total }} 条
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="changePage(pagination.page - 1)"
              :disabled="pagination.page <= 1"
              class="btn btn-sm btn-secondary"
            >
              上一页
            </button>
            <span class="text-sm text-gray-500">
              第 {{ pagination.page }} / {{ pagination.pages }} 页
            </span>
            <button
              @click="changePage(pagination.page + 1)"
              :disabled="pagination.page >= pagination.pages"
              class="btn btn-sm btn-secondary"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  ArrowPathIcon,
  TrashIcon,
  DocumentTextIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'
import { useLogs } from '@/composables/useLogs'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const {
  loading,
  logs,
  pagination,
  fetchLogs,
  clearLogs,
  changePage
} = useLogs()

// 筛选状态
const selectedMethod = ref('')
const selectedStatus = ref('')
const startDate = ref('')
const endDate = ref('')

// 展开的日志
const expandedLogs = ref(new Set<number>())

// 格式化时间
const formatTime = (dateString: string) => {
  return formatDistanceToNow(new Date(dateString), {
    addSuffix: true,
    locale: zhCN
  })
}

// 格式化JSON
const formatJson = (obj: any) => {
  if (!obj) return ''
  try {
    return JSON.stringify(obj, null, 2)
  } catch {
    return String(obj)
  }
}

// 获取状态颜色
const getStatusColor = (statusCode?: number) => {
  if (!statusCode) return 'bg-gray-400'
  if (statusCode >= 200 && statusCode < 300) return 'bg-green-400'
  if (statusCode >= 400) return 'bg-red-400'
  return 'bg-yellow-400'
}

// 切换日志详情
const toggleLogDetail = (logId: number) => {
  if (expandedLogs.value.has(logId)) {
    expandedLogs.value.delete(logId)
  } else {
    expandedLogs.value.add(logId)
  }
}

// 筛选处理
const handleFilter = () => {
  fetchLogs({
    page: 1,
    method: selectedMethod.value || undefined,
    status_code: selectedStatus.value ? Number(selectedStatus.value) : undefined,
    start_date: startDate.value || undefined,
    end_date: endDate.value || undefined
  })
}

// 重置筛选
const resetFilters = () => {
  selectedMethod.value = ''
  selectedStatus.value = ''
  startDate.value = ''
  endDate.value = ''
  fetchLogs({ page: 1 })
}

// 分页大小变化
const handlePageSizeChange = () => {
  fetchLogs({
    page: 1,
    size: pagination.size
  })
}

// 刷新数据
const refreshData = () => {
  fetchLogs()
}

// 清空日志确认
const clearLogsConfirm = () => {
  if (confirm('确定要清空所有请求日志吗？此操作不可恢复。')) {
    clearLogsHandler()
  }
}

// 清空日志处理
const clearLogsHandler = async () => {
  try {
    await clearLogs()
  } catch (error) {
    alert(`清空日志失败: ${error.message}`)
  }
}

// 初始化数据
onMounted(() => {
  fetchLogs()
})
</script>
