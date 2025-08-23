<template>
  <div class="space-y-4">
    <!-- 页面标题 -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          {{ isEdit ? '编辑Mock接口' : '创建Mock接口' }}
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          {{ isEdit ? '修改Mock接口的配置信息' : '创建一个新的Mock API接口' }}
        </p>
      </div>
      <div class="mt-4 flex space-x-3 md:mt-0 md:ml-4">
        <button
          @click="goBack"
          class="btn btn-secondary"
        >
          取消
        </button>
        <button
          @click="handleSubmit"
          :disabled="loading"
          class="btn btn-primary"
        >
          <span v-if="loading" class="loading-spinner w-4 h-4 mr-2"></span>
          {{ isEdit ? '更新接口' : '创建接口' }}
        </button>
      </div>
    </div>

    <!-- 表单内容 -->
    <div class="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <!-- 左侧：表单配置 -->
      <div class="lg:col-span-2">
        <form @submit.prevent="handleSubmit" class="space-y-3">
          <!-- 基本信息 -->
          <div class="card">
            <div class="card-header py-2">
              <h3 class="text-base font-medium text-gray-900">基本信息</h3>
              <p class="text-xs text-gray-500">配置Mock接口的基本信息</p>
            </div>
            <div class="card-body space-y-2 py-3">
              <!-- 接口名称 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">接口名称 *</label>
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="请输入接口名称，如：用户信息接口"
                  class="form-input"
                  :class="{ 'border-red-300': errors.name }"
                  required
                />
                <p v-if="errors.name" class="form-error">{{ errors.name }}</p>
              </div>

              <!-- 接口描述 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">接口描述</label>
                <input
                  v-model="form.description"
                  type="text"
                  placeholder="请输入接口描述（可选）"
                  class="form-input"
                />
              </div>

              <!-- 分类选择 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">所属分类</label>
                <select
                  v-model="form.category_id"
                  class="form-select"
                  :disabled="!!presetCategoryId"
                >
                  <option :value="undefined">未分类</option>
                  <option
                    v-for="category in flattenedCategories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ '　'.repeat(category.level) }}{{ category.name }}
                  </option>
                </select>
                <p v-if="presetCategoryId" class="text-xs text-blue-600 mt-1">
                  已自动设置为当前分类：{{ selectedCategoryName }}
                </p>
              </div>

              <!-- HTTP方法和路径 -->
              <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">HTTP方法 *</label>
                  <select
                    v-model="form.method"
                    class="form-select"
                    :class="{ 'border-red-300': errors.method }"
                    required
                  >
                    <option value="">选择方法</option>
                    <option v-for="method in httpMethods" :key="method" :value="method">
                      {{ method }}
                    </option>
                  </select>
                  <p v-if="errors.method" class="form-error">{{ errors.method }}</p>
                </div>

                <div class="sm:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-1">接口路径 *</label>
                  <div class="flex">
                    <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">
                      /mock
                    </span>
                    <input
                      v-model="form.path"
                      type="text"
                      placeholder="/users/123"
                      class="form-input rounded-l-none"
                      :class="{ 'border-red-300': errors.path }"
                      required
                    />
                  </div>
                  <p v-if="errors.path" class="form-error">{{ errors.path }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">
                    完整URL: http://localhost:8000/mock{{ form.path }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- 响应配置 -->
          <div class="card">
            <div class="card-header py-2">
              <h3 class="text-base font-medium text-gray-900">响应配置</h3>
              <p class="text-xs text-gray-500">配置Mock接口的响应内容</p>
            </div>
            <div class="card-body space-y-3 py-3">
              <!-- 状态码和接口状态 -->
              <div class="flex items-center space-x-6">
                <div class="flex-1">
                  <label class="block text-sm font-medium text-gray-700 mb-1">HTTP状态码</label>
                  <select v-model="form.status_code" class="form-select">
                    <option value="200">200 - OK</option>
                    <option value="201">201 - Created</option>
                    <option value="400">400 - Bad Request</option>
                    <option value="401">401 - Unauthorized</option>
                    <option value="403">403 - Forbidden</option>
                    <option value="404">404 - Not Found</option>
                    <option value="500">500 - Internal Server Error</option>
                  </select>
                </div>
                <div class="flex items-center mt-6">
                  <label class="flex items-center">
                    <input
                      v-model="form.is_active"
                      type="checkbox"
                      class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span class="ml-2 text-sm text-gray-700">启用此Mock接口</span>
                  </label>
                </div>
              </div>

              <!-- 响应头 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">响应头</label>
                <div class="space-y-2">
                  <div 
                    v-for="(header, index) in responseHeaders" 
                    :key="index"
                    class="flex space-x-2"
                  >
                    <input
                      v-model="header.key"
                      type="text"
                      placeholder="Header名称"
                      class="form-input flex-1"
                    />
                    <input
                      v-model="header.value"
                      type="text"
                      placeholder="Header值"
                      class="form-input flex-1"
                    />
                    <button
                      @click="removeHeader(index)"
                      type="button"
                      class="btn btn-sm btn-secondary"
                    >
                      删除
                    </button>
                  </div>
                  <button
                    @click="addHeader"
                    type="button"
                    class="btn btn-sm btn-secondary"
                  >
                    <PlusIcon class="h-4 w-4 mr-1" />
                    添加响应头
                  </button>
                </div>
              </div>

              <!-- 响应体 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">响应体 (JSON格式)</label>
                <textarea
                  v-model="responseBodyText"
                  rows="30"
                  placeholder='{"message": "Hello World", "data": {}}'
                  class="form-textarea font-mono text-sm"
                  style="min-height: 600px; resize: vertical;"
                  :class="{ 'border-red-300': errors.response_body }"
                ></textarea>
                <p v-if="errors.response_body" class="form-error">{{ errors.response_body }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  请输入有效的JSON格式数据，可拖拽调整编辑器高度
                </p>
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- 右侧：预览和测试 -->
      <div class="lg:col-span-1">
        <div class="sticky top-4 space-y-4">
          <!-- 接口预览 -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-gray-900">接口预览</h3>
            </div>
            <div class="card-body">
              <div class="space-y-3">
                <div>
                  <span class="text-sm text-gray-500">接口名称:</span>
                  <p class="font-medium">{{ form.name || '未设置' }}</p>
                </div>
                <div>
                  <span class="text-sm text-gray-500">请求方式:</span>
                  <span 
                    v-if="form.method"
                    :class="[
                      'badge ml-2',
                      form.method === 'GET' ? 'badge-success' :
                      form.method === 'POST' ? 'badge-info' :
                      form.method === 'PUT' ? 'badge-warning' :
                      form.method === 'DELETE' ? 'badge-danger' :
                      'badge-gray'
                    ]"
                  >
                    {{ form.method }}
                  </span>
                  <span v-else class="text-gray-400 ml-2">未设置</span>
                </div>
                <div>
                  <span class="text-sm text-gray-500">接口路径:</span>
                  <p class="font-mono text-sm">{{ form.path || '未设置' }}</p>
                </div>
                <div>
                  <span class="text-sm text-gray-500">状态码:</span>
                  <span class="ml-2">{{ form.status_code }}</span>
                </div>
                <div>
                  <span class="text-sm text-gray-500">所属分类:</span>
                  <span class="ml-2 text-gray-700">{{ selectedCategoryName }}</span>
                </div>
                <div>
                  <span class="text-sm text-gray-500">状态:</span>
                  <span 
                    :class="[
                      'ml-2',
                      form.is_active ? 'text-green-600' : 'text-gray-500'
                    ]"
                  >
                    {{ form.is_active ? '已启用' : '已禁用' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 快速测试 -->
          <div class="card" v-if="form.method && form.path">
            <div class="card-header">
              <h3 class="text-lg font-medium text-gray-900">快速测试</h3>
            </div>
            <div class="card-body">
              <button
                @click="testInterface"
                :disabled="!canTest"
                class="btn btn-primary w-full"
              >
                <PlayIcon class="h-4 w-4 mr-2" />
                测试接口
              </button>
              <p class="text-xs text-gray-500 mt-2">
                保存后可以测试接口响应
              </p>
            </div>
          </div>

          <!-- 使用示例 -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-gray-900">使用示例</h3>
            </div>
            <div class="card-body">
              <div class="space-y-3">
                <div>
                  <span class="text-sm text-gray-500">cURL命令:</span>
                  <div class="mt-1 p-2 bg-gray-900 text-gray-100 rounded text-xs font-mono overflow-x-auto">
                    curl -X {{ form.method || 'GET' }} \<br/>
                    &nbsp;&nbsp;http://localhost:8000/mock{{ form.path || '/path' }}
                  </div>
                </div>
                <div>
                  <span class="text-sm text-gray-500">JavaScript:</span>
                  <div class="mt-1 p-2 bg-gray-900 text-gray-100 rounded text-xs font-mono overflow-x-auto">
                    fetch('/mock{{ form.path || '/path' }}', {<br/>
                    &nbsp;&nbsp;method: '{{ form.method || 'GET' }}'<br/>
                    })
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PlusIcon, PlayIcon } from '@heroicons/vue/24/outline'
import { useMocks } from '@/composables/useMocks'
import { useCategories } from '@/composables/useCategories'
import type { MockAPICreate, MockAPIUpdate } from '@/types/mock'

const route = useRoute()
const router = useRouter()

const {
  loading,
  currentMock,
  httpMethods,
  fetchMock,
  createMock,
  updateMock,
  testMock
} = useMocks()

// 使用分类组合函数
const {
  categoryTree,
  flattenedCategories,
  findCategoryById,
  fetchCategoryTree
} = useCategories()

// 表单数据
const form = reactive<MockAPICreate & { id?: number }>({
  name: '',
  description: '',
  method: 'GET',
  path: '',
  status_code: 200,
  response_headers: {},
  response_body: {},
  is_active: true,
  category_id: undefined
})

// 预设分类ID（来自路由参数）
const presetCategoryId = computed(() => {
  const categoryId = route.params.categoryId
  if (categoryId && categoryId !== 'create') {
    return Number(categoryId)
  }
  return null
})

// 当前选中的分类名称
const selectedCategoryName = computed(() => {
  if (!form.category_id) return '未分类'
  const category = findCategoryById(form.category_id)
  return category ? category.full_path : '未知分类'
})

// 响应头管理
const responseHeaders = ref([
  { key: 'Content-Type', value: 'application/json' }
])

// 响应体文本
const responseBodyText = ref('{\n  "message": "Hello World",\n  "data": {}\n}')

// 表单验证错误
const errors = reactive({
  name: '',
  method: '',
  path: '',
  response_body: ''
})

// 计算属性
const isEdit = computed(() => !!route.params.id)
const canTest = computed(() => form.method && form.path && !isEdit.value)

// 返回上一页
const goBack = () => {
  router.back()
}

// 添加响应头
const addHeader = () => {
  responseHeaders.value.push({ key: '', value: '' })
}

// 删除响应头
const removeHeader = (index: number) => {
  responseHeaders.value.splice(index, 1)
}

// 验证表单
const validateForm = () => {
  // 重置错误
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  // 验证名称
  if (!form.name.trim()) {
    errors.name = '请输入接口名称'
    isValid = false
  }

  // 验证方法
  if (!form.method) {
    errors.method = '请选择HTTP方法'
    isValid = false
  }

  // 验证路径
  if (!form.path.trim()) {
    errors.path = '请输入接口路径'
    isValid = false
  } else if (!form.path.startsWith('/')) {
    errors.path = '路径必须以 / 开头'
    isValid = false
  }

  // 验证响应体JSON格式
  try {
    JSON.parse(responseBodyText.value)
  } catch (e) {
    errors.response_body = '响应体必须是有效的JSON格式'
    isValid = false
  }

  return isValid
}

// 处理表单提交
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  try {
    // 处理响应头
    const headers = {}
    responseHeaders.value.forEach(header => {
      if (header.key && header.value) {
        headers[header.key] = header.value
      }
    })

    // 处理响应体
    const responseBody = JSON.parse(responseBodyText.value)

    const data = {
      ...form,
      response_headers: headers,
      response_body: responseBody,
      // 确保分类ID正确设置
      category_id: form.category_id || presetCategoryId.value || undefined
    }
    
    console.log('提交数据:', data)
    console.log('当前form.category_id:', form.category_id)
    console.log('当前presetCategoryId:', presetCategoryId.value)

    if (isEdit.value) {
      await updateMock(Number(route.params.id), data as MockAPIUpdate)
    } else {
      await createMock(data)
    }

    router.push('/mocks')
  } catch (error) {
    alert(`操作失败: ${error.message}`)
  }
}

// 测试接口
const testInterface = async () => {
  if (!canTest.value) return

  try {
    const result = await testMock(form.path, form.method)
    alert(`测试成功！响应: ${JSON.stringify(result, null, 2)}`)
  } catch (error) {
    alert(`测试失败: ${error.message}`)
  }
}

// 监听响应头变化
watch(responseHeaders, (newHeaders) => {
  const headers = {}
  newHeaders.forEach(header => {
    if (header.key && header.value) {
      headers[header.key] = header.value
    }
  })
  form.response_headers = headers
}, { deep: true })

// 初始化数据
onMounted(async () => {
  // 获取分类数据
  try {
    await fetchCategoryTree()
  } catch (error) {
    console.warn('获取分类数据失败:', error)
  }

  // 如果有预设分类ID，设置到表单中
  if (presetCategoryId.value) {
    console.log('设置预设分类ID:', presetCategoryId.value)
    form.category_id = presetCategoryId.value
  }
  
  console.log('初始化完成，表单category_id:', form.category_id)

  if (isEdit.value) {
    try {
      const mock = await fetchMock(Number(route.params.id))
      
      // 填充表单数据
      Object.assign(form, mock)
      
      // 填充响应头
      responseHeaders.value = Object.entries(mock.response_headers || {}).map(([key, value]) => ({
        key,
        value: String(value)
      }))
      
      if (responseHeaders.value.length === 0) {
        responseHeaders.value.push({ key: 'Content-Type', value: 'application/json' })
      }
      
      // 填充响应体
      responseBodyText.value = JSON.stringify(mock.response_body || {}, null, 2)
      
    } catch (error) {
      alert(`加载Mock接口失败: ${error.message}`)
      router.push('/mocks')
    }
  }
})
</script>
