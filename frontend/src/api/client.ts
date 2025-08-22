/**
 * HTTP客户端配置
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import type { ApiResponse, ApiError } from '@/types/api'

class ApiClient {
  private instance: AxiosInstance

  constructor(baseURL: string = '/api/v1') {
    this.instance = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 可以在这里添加认证token等
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => {
        return response
      },
      (error) => {
        const apiError: ApiError = {
          message: error.message || '请求失败',
          status: error.response?.status,
          detail: error.response?.data?.detail || error.response?.data?.message,
        }
        
        // 统一错误处理
        if (error.response?.status === 401) {
          // 处理未授权
          console.error('未授权访问')
        } else if (error.response?.status >= 500) {
          // 处理服务器错误
          console.error('服务器错误:', apiError.detail)
        }

        return Promise.reject(apiError)
      }
    )
  }

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.get<T>(url, config)
    return response.data
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.post<T>(url, data, config)
    return response.data
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.put<T>(url, data, config)
    return response.data
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.delete<T>(url, config)
    return response.data
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.instance.patch<T>(url, data, config)
    return response.data
  }
}

// 创建默认实例
export const apiClient = new ApiClient()

// 导出类型
export type { ApiResponse, ApiError }
