<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- 页面标题栏 -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex-1 min-w-0">
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Mock接口管理
          </h2>
          <p class="mt-1 text-sm text-gray-500">
            管理您的Mock API接口，支持分类、创建、编辑、删除和测试
          </p>
        </div>
        <div class="flex items-center space-x-3">
          <button
            @click="showCategoryModal = true"
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h2a2 2 0 012 2v0H8v0z"></path>
            </svg>
            管理分类
          </button>
          <RouterLink
            to="/mocks/create"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            创建Mock接口
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- 主体内容 - 左右分栏 -->
    <div class="flex-1 flex overflow-hidden">
      <!-- 左侧分类导航 -->
      <div class="w-64 bg-white border-r border-gray-200 flex-shrink-0">
        <CategoryTree
          ref="categoryTreeRef"
          :selected-category-id="selectedCategoryId"
          :total-mock-count="totalCount"
          :uncategorized-count="uncategorizedCount"
          @select-category="handleCategorySelect"
          @manage-categories="showCategoryModal = true"
        />
      </div>

      <!-- 右侧接口列表 -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- 搜索和筛选栏 -->
        <div class="bg-white border-b border-gray-200 px-6 py-4">
          <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
            <!-- 搜索框 -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">搜索接口</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                </div>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="搜索接口名称或路径..."
                  class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  @keyup.enter="handleSearch"
                />
              </div>
            </div>

            <!-- 方法筛选 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">HTTP方法</label>
              <select 
                v-model="selectedMethod" 
                class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                @change="handleFilter"
              >
                <option value="">全部方法</option>
                <option value="GET">GET</option>
                <option value="POST">POST</option>
                <option value="PUT">PUT</option>
                <option value="DELETE">DELETE</option>
                <option value="PATCH">PATCH</option>
              </select>
            </div>

            <!-- 状态筛选 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
              <select 
                v-model="selectedStatus" 
                class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                @change="handleFilter"
              >
                <option value="">全部状态</option>
                <option value="true">已启用</option>
                <option value="false">已禁用</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 接口列表区域 -->
        <div class="flex-1 overflow-y-auto bg-white">
          <!-- 错误提示 -->
          <div v-if="error" class="p-6">
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {{ error }}
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else-if="!loading && mocks.length === 0" class="p-12">
            <div class="text-center">
              <svg class="h-12 w-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                {{ selectedCategoryId !== null ? '该分类下暂无接口' : '暂无Mock接口' }}
              </h3>
              <p class="text-gray-500 mb-6">
                {{ selectedCategoryId !== null ? '请在其他分类中查找或添加新接口' : '开始创建您的第一个Mock接口吧' }}
              </p>
              <RouterLink 
                to="/mocks/create" 
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                创建Mock接口
              </RouterLink>
            </div>
          </div>

          <!-- 接口列表 -->
          <div v-else>
            <!-- 列表头部 -->
            <div class="sticky top-0 bg-gray-50 border-b border-gray-200 px-6 py-3">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900">
                  {{ getCurrentCategoryName() }} ({{ mocks.length }})
                  <span v-if="loading" class="ml-2 text-sm text-gray-500">加载中...</span>
                </h3>
                <div class="flex items-center space-x-2">
                  <button
                    @click="refreshData"
                    :disabled="loading"
                    class="text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50"
                    title="刷新列表"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- 接口表格 -->
            <div class="overflow-x-auto">
              <table class="min-w-full">
                <thead class="bg-gray-50 sticky top-16">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">接口信息</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">方法</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">路径</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr 
                    v-for="mock in filteredMocks" 
                    :key="mock.id"
                    class="hover:bg-gray-50"
                  >
                    <!-- 接口信息 -->
                    <td class="px-6 py-4">
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ mock.name }}</div>
                        <div class="text-sm text-gray-500">{{ mock.description || '无描述' }}</div>
                      </div>
                    </td>

                    <!-- HTTP方法 -->
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span 
                        :class="[
                          'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                          mock.method === 'GET' ? 'bg-green-100 text-green-800' :
                          mock.method === 'POST' ? 'bg-blue-100 text-blue-800' :
                          mock.method === 'PUT' ? 'bg-yellow-100 text-yellow-800' :
                          mock.method === 'DELETE' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        ]"
                      >
                        {{ mock.method }}
                      </span>
                    </td>

                    <!-- 路径 -->
                    <td class="px-6 py-4 whitespace-nowrap">
                      <code class="text-sm bg-gray-100 px-2 py-1 rounded">{{ mock.path }}</code>
                    </td>

                    <!-- 状态 -->
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div 
                          :class="[
                            'w-2 h-2 rounded-full mr-2',
                            mock.is_active ? 'bg-green-400' : 'bg-gray-400'
                          ]"
                        ></div>
                        <span :class="mock.is_active ? 'text-green-700' : 'text-gray-500'">
                          {{ mock.is_active ? '已启用' : '已禁用' }}
                        </span>
                      </div>
                    </td>

                    <!-- 操作 -->
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div class="flex items-center space-x-3">
                        <!-- 测试按钮 -->
                        <button
                          @click="testMock(mock)"
                          class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-sm transition-colors duration-200"
                          title="测试接口"
                        >
                          <svg class="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                          </svg>
                          测试
                        </button>
                        
                        <!-- 详情按钮 -->
                        <RouterLink
                          :to="`/mocks/${mock.id}`"
                          class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 shadow-sm transition-colors duration-200"
                          title="查看详情"
                        >
                          <svg class="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                          </svg>
                          详情
                        </RouterLink>
                        
                        <!-- 编辑按钮 -->
                        <RouterLink
                          :to="`/mocks/${mock.id}/edit`"
                          class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm transition-colors duration-200"
                          title="编辑"
                        >
                          <svg class="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                          </svg>
                          编辑
                        </RouterLink>
                        
                        <!-- 删除按钮 -->
                        <button
                          @click="deleteMock(mock)"
                          class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 shadow-sm transition-colors duration-200"
                          title="删除"
                        >
                          <svg class="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                          删除
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类管理弹窗 -->
    <CategoryModal
      :visible="showCategoryModal"
      @close="showCategoryModal = false"
      @updated="handleCategoryUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useMocks } from '@/composables/useMocks'
import { useCategories } from '@/composables/useCategories'
import { CategoryTree } from '@/components/CategoryTree'
import { CategoryModal } from '@/components/CategoryModal'

// 搜索和筛选状态
const searchQuery = ref('')
const selectedMethod = ref('')
const selectedStatus = ref('')
const selectedCategoryId = ref<number | null>(null)

// 分类弹窗状态
const showCategoryModal = ref(false)

// 分类树引用
const categoryTreeRef = ref()

// 使用Mock接口组合函数
const {
  loading,
  error,
  mocks,
  query,
  fetchMocks,
  deleteMock: deleteMockApi,
  testMock: testMockApi
} = useMocks()

// 使用分类组合函数
const {
  findCategoryById
} = useCategories()

// 筛选后的Mock列表
const filteredMocks = computed(() => {
  return mocks.value.filter(mock => {
    const matchesSearch = !searchQuery.value || 
      mock.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      mock.path.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesMethod = !selectedMethod.value || mock.method === selectedMethod.value
    
    const matchesStatus = !selectedStatus.value || 
      (selectedStatus.value === 'true' && mock.is_active) ||
      (selectedStatus.value === 'false' && !mock.is_active)
    
    return matchesSearch && matchesMethod && matchesStatus
  })
})

// 总接口数和未分类接口数
const totalCount = computed(() => mocks.value.length)
const uncategorizedCount = computed(() => 
  mocks.value.filter(mock => !mock.category_id).length
)

// 获取当前分类名称
const getCurrentCategoryName = () => {
  if (selectedCategoryId.value === null) {
    return '全部接口'
  }
  if (selectedCategoryId.value === 0) {
    return '未分类接口'
  }
  
  const category = findCategoryById(selectedCategoryId.value)
  return category ? category.name : '接口列表'
}

// 处理分类选择
const handleCategorySelect = (categoryId: number | null) => {
  selectedCategoryId.value = categoryId
  query.category_id = categoryId
  refreshData()
}

// 搜索处理
const handleSearch = () => {
  query.search = searchQuery.value
  refreshData()
}

// 筛选处理
const handleFilter = () => {
  query.method = selectedMethod.value || undefined
  query.is_active = selectedStatus.value ? selectedStatus.value === 'true' : undefined
  refreshData()
}

// 刷新数据
const refreshData = async () => {
  try {
    await fetchMocks(query)
  } catch (err) {
    console.error('刷新数据失败:', err)
  }
}

// 测试Mock接口
const testMock = async (mock: any) => {
  try {
    const result = await testMockApi(mock.path, mock.method)
    alert(`测试成功！响应: ${JSON.stringify(result, null, 2)}`)
  } catch (err: any) {
    alert(`测试失败: ${err.message}`)
  }
}

// 删除Mock接口
const deleteMock = async (mock: any) => {
  if (confirm(`确定要删除Mock接口 "${mock.name}" 吗？`)) {
    try {
      await deleteMockApi(mock.id)
      refreshData()
    } catch (err: any) {
      alert(`删除失败: ${err.message}`)
    }
  }
}

// 处理分类更新
const handleCategoryUpdated = () => {
  // 刷新分类树
  if (categoryTreeRef.value?.refresh) {
    categoryTreeRef.value.refresh()
  }
  // 如果当前选中的是某个分类，刷新接口列表
  refreshData()
}

// 监听搜索和筛选条件变化
watch([searchQuery, selectedMethod, selectedStatus], () => {
  handleFilter()
}, { debounce: 300 })

// 组件挂载时获取数据
onMounted(async () => {
  try {
    await fetchMocks()
  } catch (err) {
    console.error('初始化数据失败:', err)
  }
})
</script>
