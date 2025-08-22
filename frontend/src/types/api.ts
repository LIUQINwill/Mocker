/**
 * API响应相关类型定义
 */

export interface ApiResponse<T = any> {
  data: T
  message?: string
  success: boolean
}

export interface ApiError {
  message: string
  detail?: string
  status?: number
}

export interface PaginationParams {
  page?: number
  size?: number
}

export interface SearchParams {
  search?: string
  [key: string]: any
}
