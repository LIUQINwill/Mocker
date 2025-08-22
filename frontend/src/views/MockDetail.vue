<template>
  <div class="space-y-6">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="loading-spinner w-8 h-8"></div>
      <span class="ml-2 text-gray-500">加载中...</span>
    </div>

    <!-- Mock接口详情 -->
    <div v-else-if="currentMock" class="space-y-6">
      <!-- 页面标题和操作 -->
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex-1 min-w-0">
          <div class="flex items-center space-x-3">
            <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              {{ currentMock.name }}
            </h2>
            <span 
              :class="[
                'badge',
                currentMock.method === 'GET' ? 'badge-success' :
                currentMock.method === 'POST' ? 'badge-info' :
                currentMock.method === 'PUT' ? 'badge-warning' :
                currentMock.method === 'DELETE' ? 'badge-danger' :
                'badge-gray'
              ]"
            >
              {{ currentMock.method }}
            </span>
            <div class="flex items-center">
              <div 
                :class="[
                  'status-dot mr-2',
                  currentMock.is_active ? 'status-dot-success' : 'status-dot-gray'
                ]"
              ></div>
              <span :class="currentMock.is_active ? 'text-green-700' : 'text-gray-500'">
                {{ currentMock.is_active ? '已启用' : '已禁用' }}
              </span>
            </div>
          </div>
          <p class="mt-1 text-sm text-gray-500">
            {{ currentMock.description || '无描述' }}
          </p>
        </div>
        <div class="mt-4 flex space-x-3 md:mt-0 md:ml-4">
          <button
            @click="testMockInterface"
            class="btn btn-secondary"
          >
            <PlayIcon class="h-4 w-4 mr-2" />
            测试接口
          </button>
          <RouterLink
            :to="`/mocks/${currentMock.id}/edit`"
            class="btn btn-primary"
          >
            <PencilIcon class="h-4 w-4 mr-2" />
            编辑接口
          </RouterLink>
        </div>
      </div>

      <!-- 接口信息卡片 -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- 基本信息 -->
        <div class="card">
          <div class="card-header">
            <h3 class="text-lg font-medium text-gray-900">基本信息</h3>
          </div>
          <div class="card-body">
            <dl class="space-y-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">接口名称</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ currentMock.name }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">接口描述</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ currentMock.description || '无描述' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">HTTP方法</dt>
                <dd class="mt-1">
                  <span 
                    :class="[
                      'badge',
                      currentMock.method === 'GET' ? 'badge-success' :
                      currentMock.method === 'POST' ? 'badge-info' :
                      currentMock.method === 'PUT' ? 'badge-warning' :
                      currentMock.method === 'DELETE' ? 'badge-danger' :
                      'badge-gray'
                    ]"
                  >
                    {{ currentMock.method }}
                  </span>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">接口路径</dt>
                <dd class="mt-1">
                  <code class="text-sm bg-gray-100 px-2 py-1 rounded">{{ currentMock.path }}</code>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">完整URL</dt>
                <dd class="mt-1">
                  <code class="text-sm bg-gray-100 px-2 py-1 rounded break-all">
                    http://localhost:8000/mock{{ currentMock.path }}
                  </code>
                  <button
                    @click="copyUrl"
                    class="ml-2 text-primary-600 hover:text-primary-500 text-sm"
                    title="复制URL"
                  >
                    <ClipboardIcon class="h-4 w-4" />
                  </button>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">状态码</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ currentMock.status_code }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">状态</dt>
                <dd class="mt-1">
                  <div class="flex items-center">
                    <div 
                      :class="[
                        'status-dot mr-2',
                        currentMock.is_active ? 'status-dot-success' : 'status-dot-gray'
                      ]"
                    ></div>
                    <span :class="currentMock.is_active ? 'text-green-700' : 'text-gray-500'">
                      {{ currentMock.is_active ? '已启用' : '已禁用' }}
                    </span>
                  </div>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">创建时间</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatTime(currentMock.created_at) }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">更新时间</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatTime(currentMock.updated_at) }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <!-- 使用示例 -->
        <div class="card">
          <div class="card-header">
            <h3 class="text-lg font-medium text-gray-900">使用示例</h3>
          </div>
          <div class="card-body space-y-4">
            <!-- cURL示例 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-2">cURL命令</h4>
              <div class="relative">
                <pre class="code-block">curl -X {{ currentMock.method }} \
  http://localhost:8000/mock{{ currentMock.path }}</pre>
                <button
                  @click="copyCurl"
                  class="absolute top-2 right-2 text-gray-400 hover:text-gray-300"
                  title="复制cURL命令"
                >
                  <ClipboardIcon class="h-4 w-4" />
                </button>
              </div>
            </div>

            <!-- JavaScript示例 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-2">JavaScript (Fetch)</h4>
              <div class="relative">
                <pre class="code-block">fetch('/mock{{ currentMock.path }}', {
  method: '{{ currentMock.method }}'
})
.then(response => response.json())
.then(data => console.log(data))</pre>
                <button
                  @click="copyJavaScript"
                  class="absolute top-2 right-2 text-gray-400 hover:text-gray-300"
                  title="复制JavaScript代码"
                >
                  <ClipboardIcon class="h-4 w-4" />
                </button>
              </div>
            </div>

            <!-- Python示例 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-2">Python (requests)</h4>
              <div class="relative">
                <pre class="code-block">import requests

response = requests.{{ currentMock.method.toLowerCase() }}(
    'http://localhost:8000/mock{{ currentMock.path }}'
)
print(response.json())</pre>
                <button
                  @click="copyPython"
                  class="absolute top-2 right-2 text-gray-400 hover:text-gray-300"
                  title="复制Python代码"
                >
                  <ClipboardIcon class="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 响应配置 -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">响应配置</h3>
        </div>
        <div class="card-body">
          <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <!-- 响应头 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">响应头</h4>
              <div v-if="currentMock.response_headers && Object.keys(currentMock.response_headers).length > 0">
                <pre class="code-block">{{ formatJson(currentMock.response_headers) }}</pre>
              </div>
              <div v-else class="text-sm text-gray-500">
                无自定义响应头
              </div>
            </div>

            <!-- 响应体 -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">响应体</h4>
              <div v-if="currentMock.response_body">
                <pre class="code-block">{{ formatJson(currentMock.response_body) }}</pre>
              </div>
              <div v-else class="text-sm text-gray-500">
                无响应体
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="text-center py-12">
      <ExclamationTriangleIcon class="h-12 w-12 text-red-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">加载失败</h3>
      <p class="text-gray-500 mb-6">无法加载Mock接口详情</p>
      <RouterLink to="/mocks" class="btn btn-primary">
        返回列表
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import {
  PlayIcon,
  PencilIcon,
  ClipboardIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import { useMocks } from '@/composables/useMocks'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const route = useRoute()

const {
  loading,
  currentMock,
  fetchMock,
  testMock
} = useMocks()

// 格式化时间
const formatTime = (dateString: string) => {
  return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss', { locale: zhCN })
}

// 格式化JSON
const formatJson = (obj: any) => {
  return JSON.stringify(obj, null, 2)
}

// 复制到剪贴板
const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    alert('已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    alert('复制失败，请手动复制')
  }
}

// 复制URL
const copyUrl = () => {
  if (currentMock.value) {
    copyToClipboard(`http://localhost:8000/mock${currentMock.value.path}`)
  }
}

// 复制cURL命令
const copyCurl = () => {
  if (currentMock.value) {
    const curl = `curl -X ${currentMock.value.method} http://localhost:8000/mock${currentMock.value.path}`
    copyToClipboard(curl)
  }
}

// 复制JavaScript代码
const copyJavaScript = () => {
  if (currentMock.value) {
    const js = `fetch('/mock${currentMock.value.path}', {
  method: '${currentMock.value.method}'
})
.then(response => response.json())
.then(data => console.log(data))`
    copyToClipboard(js)
  }
}

// 复制Python代码
const copyPython = () => {
  if (currentMock.value) {
    const python = `import requests

response = requests.${currentMock.value.method.toLowerCase()}(
    'http://localhost:8000/mock${currentMock.value.path}'
)
print(response.json())`
    copyToClipboard(python)
  }
}

// 测试Mock接口
const testMockInterface = async () => {
  if (!currentMock.value) return

  try {
    const result = await testMock(currentMock.value.path, currentMock.value.method)
    alert(`测试成功！响应: ${JSON.stringify(result, null, 2)}`)
  } catch (error) {
    alert(`测试失败: ${error.message}`)
  }
}

// 初始化数据
onMounted(async () => {
  const id = Number(route.params.id)
  if (id) {
    try {
      await fetchMock(id)
    } catch (error) {
      console.error('加载Mock接口失败:', error)
    }
  }
})
</script>
