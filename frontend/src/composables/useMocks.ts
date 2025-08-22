/**
 * Mock接口相关组合式函数
 */
import { ref, reactive, computed } from 'vue'
import { mockApi } from '@/api/mocks'
import type {
  MockAPI,
  MockAPICreate,
  MockAPIUpdate,
  MockAPIQuery,
  HTTPMethod
} from '@/types/mock'

export function useMocks() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const mocks = ref<MockAPI[]>([])
  const currentMock = ref<MockAPI | null>(null)
  const pagination = reactive({
    total: 0,
    page: 1,
    size: 20,
    pages: 0
  })

  // 查询参数
  const query = reactive<MockAPIQuery>({
    page: 1,
    size: 20,
    search: '',
    method: undefined,
    is_active: undefined,
    category_id: undefined
  })

  // 计算属性
  const activeMocks = computed(() =>
    mocks.value.filter(mock => mock.is_active)
  )

  const inactiveMocks = computed(() =>
    mocks.value.filter(mock => !mock.is_active)
  )

  // HTTP方法选项
  const httpMethods: HTTPMethod[] = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']

  /**
   * 获取Mock接口列表
   */
  const fetchMocks = async (params?: MockAPIQuery) => {
    try {
      loading.value = true
      error.value = null

      const queryParams = { ...query, ...params }
      const result = await mockApi.list(queryParams)

      mocks.value = result.items
      pagination.total = result.total
      pagination.page = result.page
      pagination.size = result.size
      pagination.pages = result.pages

      return result
    } catch (err: any) {
      error.value = err.message || '获取Mock接口列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取Mock接口详情
   */
  const fetchMock = async (id: number) => {
    try {
      loading.value = true
      error.value = null

      const result = await mockApi.get(id)
      currentMock.value = result

      return result
    } catch (err: any) {
      error.value = err.message || '获取Mock接口详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 创建Mock接口
   */
  const createMock = async (data: MockAPICreate) => {
    try {
      loading.value = true
      error.value = null

      const result = await mockApi.create(data)

      // 刷新列表
      await fetchMocks()

      return result
    } catch (err: any) {
      error.value = err.message || '创建Mock接口失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新Mock接口
   */
  const updateMock = async (id: number, data: MockAPIUpdate) => {
    try {
      loading.value = true
      error.value = null

      const result = await mockApi.update(id, data)

      // 更新本地数据
      const index = mocks.value.findIndex(mock => mock.id === id)
      if (index !== -1) {
        mocks.value[index] = result
      }

      if (currentMock.value?.id === id) {
        currentMock.value = result
      }

      return result
    } catch (err: any) {
      error.value = err.message || '更新Mock接口失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 删除Mock接口
   */
  const deleteMock = async (id: number) => {
    try {
      loading.value = true
      error.value = null

      await mockApi.delete(id)

      // 从本地数据中移除
      mocks.value = mocks.value.filter(mock => mock.id !== id)
      pagination.total -= 1

      if (currentMock.value?.id === id) {
        currentMock.value = null
      }

    } catch (err: any) {
      error.value = err.message || '删除Mock接口失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 切换Mock接口状态
   */
  const toggleMock = async (id: number) => {
    try {
      loading.value = true
      error.value = null

      const result = await mockApi.toggle(id)

      // 更新本地数据
      const index = mocks.value.findIndex(mock => mock.id === id)
      if (index !== -1) {
        mocks.value[index] = result
      }

      if (currentMock.value?.id === id) {
        currentMock.value = result
      }

      return result
    } catch (err: any) {
      error.value = err.message || '切换Mock接口状态失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 测试Mock接口
   */
  const testMock = async (path: string, method: string = 'GET', data?: any) => {
    try {
      loading.value = true
      error.value = null

      const result = await mockApi.test(path, method, data)
      return result
    } catch (err: any) {
      error.value = err.message || '测试Mock接口失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 搜索Mock接口
   */
  const searchMocks = async (searchText: string) => {
    query.search = searchText
    query.page = 1
    await fetchMocks()
  }

  /**
   * 筛选Mock接口
   */
  const filterMocks = async (filters: Partial<MockAPIQuery>) => {
    Object.assign(query, filters)
    query.page = 1
    await fetchMocks()
  }

  /**
   * 分页
   */
  const changePage = async (page: number) => {
    query.page = page
    await fetchMocks()
  }

  /**
   * 重置查询
   */
  const resetQuery = () => {
    Object.assign(query, {
      page: 1,
      size: 20,
      search: '',
      method: undefined,
      is_active: undefined
    })
  }

  return {
    // 状态
    loading,
    error,
    mocks,
    currentMock,
    pagination,
    query,

    // 计算属性
    activeMocks,
    inactiveMocks,
    httpMethods,

    // 方法
    fetchMocks,
    fetchMock,
    createMock,
    updateMock,
    deleteMock,
    toggleMock,
    testMock,
    searchMocks,
    filterMocks,
    changePage,
    resetQuery
  }
}
