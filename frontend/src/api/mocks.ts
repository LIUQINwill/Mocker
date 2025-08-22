/**
 * Mock接口API
 */
import { apiClient } from './client'
import type { 
  MockAPI, 
  MockAPICreate, 
  MockAPIUpdate, 
  MockAPIList, 
  MockAPIQuery 
} from '@/types/mock'

export const mockApi = {
  /**
   * 获取Mock接口列表
   */
  async list(params?: MockAPIQuery): Promise<MockAPIList> {
    const searchParams = new URLSearchParams()
    
    if (params?.page) searchParams.append('page', params.page.toString())
    if (params?.size) searchParams.append('size', params.size.toString())
    if (params?.is_active !== undefined) searchParams.append('is_active', params.is_active.toString())
    if (params?.method) searchParams.append('method', params.method)
    if (params?.search) searchParams.append('search', params.search)
    if (params?.category_id !== undefined && params?.category_id !== null) searchParams.append('category_id', params.category_id.toString())

    const query = searchParams.toString()
    const url = query ? `/mocks/?${query}` : '/mocks/'
    
    return apiClient.get<MockAPIList>(url)
  },

  /**
   * 获取Mock接口详情
   */
  async get(id: number): Promise<MockAPI> {
    return apiClient.get<MockAPI>(`/mocks/${id}`)
  },

  /**
   * 创建Mock接口
   */
  async create(data: MockAPICreate): Promise<MockAPI> {
    return apiClient.post<MockAPI>('/mocks/', data)
  },

  /**
   * 更新Mock接口
   */
  async update(id: number, data: MockAPIUpdate): Promise<MockAPI> {
    return apiClient.put<MockAPI>(`/mocks/${id}`, data)
  },

  /**
   * 删除Mock接口
   */
  async delete(id: number): Promise<{ message: string }> {
    return apiClient.delete(`/mocks/${id}`)
  },

  /**
   * 切换Mock接口状态
   */
  async toggle(id: number): Promise<MockAPI> {
    return apiClient.post<MockAPI>(`/mocks/${id}/toggle`)
  },

  /**
   * 测试Mock接口
   */
  async test(path: string, method: string = 'GET', data?: any): Promise<any> {
    const mockClient = apiClient
    const url = `/mock${path}`
    
    switch (method.toUpperCase()) {
      case 'GET':
        return mockClient.get(url)
      case 'POST':
        return mockClient.post(url, data)
      case 'PUT':
        return mockClient.put(url, data)
      case 'DELETE':
        return mockClient.delete(url)
      case 'PATCH':
        return mockClient.patch(url, data)
      default:
        return mockClient.get(url)
    }
  }
}
