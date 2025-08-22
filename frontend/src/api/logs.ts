/**
 * 请求日志API
 */
import { apiClient } from './client'
import type { 
  RequestLog, 
  RequestLogList, 
  LogStats, 
  LogQuery 
} from '@/types/log'

export const logApi = {
  /**
   * 获取请求日志列表
   */
  async list(params?: LogQuery): Promise<RequestLogList> {
    const searchParams = new URLSearchParams()
    
    if (params?.page) searchParams.append('page', params.page.toString())
    if (params?.size) searchParams.append('size', params.size.toString())
    if (params?.mock_api_id !== undefined && params?.mock_api_id !== null) searchParams.append('mock_api_id', params.mock_api_id.toString())
    if (params?.method) searchParams.append('method', params.method)
    if (params?.status_code !== undefined && params?.status_code !== null) searchParams.append('status_code', params.status_code.toString())
    if (params?.start_date) searchParams.append('start_date', params.start_date)
    if (params?.end_date) searchParams.append('end_date', params.end_date)

    const query = searchParams.toString()
    const url = query ? `/logs/?${query}` : '/logs/'
    
    return apiClient.get<RequestLogList>(url)
  },

  /**
   * 获取请求日志详情
   */
  async get(id: number): Promise<RequestLog> {
    return apiClient.get<RequestLog>(`/logs/${id}`)
  },

  /**
   * 获取日志统计信息
   */
  async getStats(): Promise<LogStats> {
    return apiClient.get<LogStats>('/logs/stats/overview')
  },

  /**
   * 清空所有日志
   */
  async clear(): Promise<{ message: string }> {
    return apiClient.delete('/logs/')
  }
}
