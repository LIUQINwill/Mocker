/**
 * 请求日志相关组合式函数
 */
import { ref, reactive } from 'vue'
import { logApi } from '@/api/logs'
import type { 
  RequestLog, 
  RequestLogList, 
  LogStats, 
  LogQuery 
} from '@/types/log'

export function useLogs() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const logs = ref<RequestLog[]>([])
  const currentLog = ref<RequestLog | null>(null)
  const stats = ref<LogStats | null>(null)
  const pagination = reactive({
    total: 0,
    page: 1,
    size: 20,
    pages: 0
  })

  // 查询参数
  const query = reactive<LogQuery>({
    page: 1,
    size: 20,
    mock_api_id: undefined,
    method: undefined,
    status_code: undefined,
    start_date: undefined,
    end_date: undefined
  })

  /**
   * 获取请求日志列表
   */
  const fetchLogs = async (params?: LogQuery) => {
    try {
      loading.value = true
      error.value = null
      
      const queryParams = { ...query, ...params }
      const result = await logApi.list(queryParams)
      
      logs.value = result.items
      pagination.total = result.total
      pagination.page = result.page
      pagination.size = result.size
      pagination.pages = result.pages
      
      return result
    } catch (err: any) {
      error.value = err.message || '获取请求日志失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取请求日志详情
   */
  const fetchLog = async (id: number) => {
    try {
      loading.value = true
      error.value = null
      
      const result = await logApi.get(id)
      currentLog.value = result
      
      return result
    } catch (err: any) {
      error.value = err.message || '获取请求日志详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取日志统计信息
   */
  const fetchStats = async () => {
    try {
      loading.value = true
      error.value = null
      
      const result = await logApi.getStats()
      stats.value = result
      
      return result
    } catch (err: any) {
      error.value = err.message || '获取统计信息失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 清空所有日志
   */
  const clearLogs = async () => {
    try {
      loading.value = true
      error.value = null
      
      await logApi.clear()
      
      // 清空本地数据
      logs.value = []
      pagination.total = 0
      pagination.page = 1
      pagination.pages = 0
      
      // 刷新统计信息
      await fetchStats()
      
    } catch (err: any) {
      error.value = err.message || '清空日志失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 筛选日志
   */
  const filterLogs = async (filters: Partial<LogQuery>) => {
    Object.assign(query, filters)
    query.page = 1
    await fetchLogs()
  }

  /**
   * 分页
   */
  const changePage = async (page: number) => {
    query.page = page
    await fetchLogs()
  }

  /**
   * 重置查询
   */
  const resetQuery = () => {
    Object.assign(query, {
      page: 1,
      size: 20,
      mock_api_id: undefined,
      method: undefined,
      status_code: undefined,
      start_date: undefined,
      end_date: undefined
    })
  }

  return {
    // 状态
    loading,
    error,
    logs,
    currentLog,
    stats,
    pagination,
    query,
    
    // 方法
    fetchLogs,
    fetchLog,
    fetchStats,
    clearLogs,
    filterLogs,
    changePage,
    resetQuery
  }
}
