import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 配置 NProgress
NProgress.configure({ showSpinner: false })

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: 'DoodleSketchAI - AI视频简笔画生成工具'
    }
  },
  {
    path: '/video/editor',
    name: 'VideoEditorNew',
    component: () => import('@/views/VideoEditor.vue'),
    meta: {
      title: '视频编辑器 - DoodleSketchAI'
    }
  },
  {
    path: '/video/:id',
    name: 'VideoEditor',
    component: () => import('@/views/VideoEditor.vue'),
    meta: {
      title: '视频编辑器 - DoodleSketchAI'
    }
  },
  {
    path: '/results/:videoId',
    name: 'Results',
    component: () => import('@/views/Results.vue'),
    meta: {
      title: '生成结果 - DoodleSketchAI'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面未找到 - DoodleSketchAI'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  NProgress.start()
  
  // 设置页面标题
  if (to.meta?.title) {
    document.title = to.meta.title as string
  }
  
  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
