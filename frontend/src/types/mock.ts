/**
 * Mock接口相关类型定义
 */

export type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD' | 'OPTIONS'

export interface MockAPI {
  id: number
  name: string
  description?: string
  method: HTTPMethod
  path: string
  status_code: number
  response_headers?: Record<string, string>
  response_body?: Record<string, any>
  response_template?: string
  is_active: boolean
  version: number
  category_id?: number
  created_at: string
  updated_at: string
}

export interface MockAPICreate {
  name: string
  description?: string
  method: HTTPMethod
  path: string
  status_code?: number
  response_headers?: Record<string, string>
  response_body?: Record<string, any>
  response_template?: string
  is_active?: boolean
  category_id?: number
}

export interface MockAPIUpdate {
  name?: string
  description?: string
  method?: HTTPMethod
  path?: string
  status_code?: number
  response_headers?: Record<string, string>
  response_body?: Record<string, any>
  response_template?: string
  is_active?: boolean
  category_id?: number
}

export interface MockAPIList {
  items: MockAPI[]
  total: number
  page: number
  size: number
  pages: number
}

export interface MockAPIQuery {
  page?: number
  size?: number
  is_active?: boolean
  method?: HTTPMethod
  search?: string
  category_id?: number
}
