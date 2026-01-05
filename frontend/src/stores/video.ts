import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Video, Breakpoint, Task } from '@/types'

// 视频管理状态
export const useVideoStore = defineStore('video', () => {
  // 状态
  const videos = ref<Video[]>([])
  const currentVideo = ref<Video | null>(null)
  const currentBreakpoints = ref<Breakpoint[]>([])
  const currentTasks = ref<Task[]>([])
  const isLoading = ref(false)
  const uploadProgress = ref(0)

  // 计算属性
  const hasCurrentVideo = computed(() => !!currentVideo.value)
  
  const videoCount = computed(() => videos.value.length)
  
  const breakpointCount = computed(() => currentBreakpoints.value.length)
  
  const pendingTasksCount = computed(() => 
    currentTasks.value.filter(task => task.status === 'pending').length
  )
  
  const completedTasksCount = computed(() => 
    currentTasks.value.filter(task => task.status === 'completed').length
  )

  // Actions
  const addVideo = (video: Video) => {
    videos.value.unshift(video)
  }

  const removeVideo = (videoId: string) => {
    const index = videos.value.findIndex(v => v.id === videoId)
    if (index > -1) {
      videos.value.splice(index, 1)
    }
  }

  const setCurrentVideo = (video: Video) => {
    currentVideo.value = video
    currentBreakpoints.value = []
    currentTasks.value = []
  }

  const clearCurrentVideo = () => {
    currentVideo.value = null
    currentBreakpoints.value = []
    currentTasks.value = []
  }

  // 断点管理
  const addBreakpoint = (breakpoint: Breakpoint) => {
    if (!currentVideo.value) return
    
    currentBreakpoints.value.push(breakpoint)
    // 按时间戳排序
    currentBreakpoints.value.sort((a, b) => a.timestamp - b.timestamp)
  }

  const updateBreakpoint = (breakpointId: string, updates: Partial<Breakpoint>) => {
    const index = currentBreakpoints.value.findIndex(bp => bp.id === breakpointId)
    if (index > -1) {
      currentBreakpoints.value[index] = { ...currentBreakpoints.value[index], ...updates }
    }
  }

  const removeBreakpoint = (breakpointId: string) => {
    const index = currentBreakpoints.value.findIndex(bp => bp.id === breakpointId)
    if (index > -1) {
      currentBreakpoints.value.splice(index, 1)
    }
  }

  // 任务管理
  const addTask = (task: Task) => {
    currentTasks.value.push(task)
  }

  const updateTask = (taskId: string, updates: Partial<Task>) => {
    const index = currentTasks.value.findIndex(task => task.id === taskId)
    if (index > -1) {
      currentTasks.value[index] = { ...currentTasks.value[index], ...updates }
    }
  }

  const removeTask = (taskId: string) => {
    const index = currentTasks.value.findIndex(task => task.id === taskId)
    if (index > -1) {
      currentTasks.value.splice(index, 1)
    }
  }

  // 上传相关
  const setUploadProgress = (progress: number) => {
    uploadProgress.value = progress
  }

  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  return {
    // 状态
    videos: readonly(videos),
    currentVideo: readonly(currentVideo),
    currentBreakpoints: readonly(currentBreakpoints),
    currentTasks: readonly(currentTasks),
    isLoading: readonly(isLoading),
    uploadProgress: readonly(uploadProgress),
    
    // 计算属性
    hasCurrentVideo,
    videoCount,
    breakpointCount,
    pendingTasksCount,
    completedTasksCount,
    
    // Actions
    addVideo,
    removeVideo,
    setCurrentVideo,
    clearCurrentVideo,
    addBreakpoint,
    updateBreakpoint,
    removeBreakpoint,
    addTask,
    updateTask,
    removeTask,
    setUploadProgress,
    setLoading
  }
})
