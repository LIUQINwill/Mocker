/**
 * Vue Router 配置
 */
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/components/Layout/MainLayout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: () => import('@/views/SimpleDashboard.vue'),
          meta: {
            title: '仪表板',
            icon: 'ChartBarIcon'
          }
        },
        {
          path: '/mocks',
          name: 'MockList',
          component: () => import('@/views/SimpleMockList.vue'),
          meta: {
            title: 'Mock接口',
            icon: 'CodeBracketIcon'
          }
        },
        {
          path: '/mocks/create',
          name: 'MockCreate',
          component: () => import('@/views/MockForm.vue'),
          meta: {
            title: '创建Mock接口',
            hideInMenu: true
          }
        },
        {
          path: '/mocks/:id/edit',
          name: 'MockEdit',
          component: () => import('@/views/MockForm.vue'),
          meta: {
            title: '编辑Mock接口',
            hideInMenu: true
          }
        },
        {
          path: '/mocks/:id',
          name: 'MockDetail',
          component: () => import('@/views/MockDetail.vue'),
          meta: {
            title: 'Mock接口详情',
            hideInMenu: true
          }
        },
        {
          path: '/logs',
          name: 'LogList',
          component: () => import('@/views/LogList.vue'),
          meta: {
            title: '请求日志',
            icon: 'DocumentTextIcon'
          }
        },
        {
          path: '/test',
          name: 'TestTailwind',
          component: () => import('@/views/TestTailwind.vue'),
          meta: {
            title: '样式测试',
            hideInMenu: true
          }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue')
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - Mocker Platform`
  } else {
    document.title = 'Mocker Platform'
  }
  
  next()
})

export default router
