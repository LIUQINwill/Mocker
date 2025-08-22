/**
 * 请求日志相关类型定义
 */

export interface RequestLog {
  id: number
  mock_api_id?: number
  request_method: string
  request_path: string
  request_headers?: Record<string, any>
  request_body?: Record<string, any>
  request_params?: Record<string, any>
  response_status_code?: number
  response_headers?: Record<string, any>
  response_body?: Record<string, any>
  response_time_ms?: number
  client_ip?: string
  user_agent?: string
  created_at: string
}

export interface RequestLogList {
  items: RequestLog[]
  total: number
  page: number
  size: number
  pages: number
}

export interface LogStats {
  total_requests: number
  today_requests: number
  success_rate: number
  avg_response_time: number
  top_apis: Array<{
    path: string
    method: string
    count: number
  }>
  method_stats: Record<string, number>
  status_stats: Record<string, number>
}

export interface LogQuery {
  page?: number
  size?: number
  mock_api_id?: number
  method?: string
  status_code?: number
  start_date?: string
  end_date?: string
}
