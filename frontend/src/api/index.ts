import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse, ApiError } from '@/types'

// 创建 axios 实例
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加认证 token
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加请求时间戳
    config.metadata = { startTime: new Date() }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const endTime = new Date()
    const startTime = response.config.metadata?.startTime
    if (startTime) {
      const duration = endTime.getTime() - startTime.getTime()
      console.log(`API request completed in ${duration}ms:`, response.config.url)
    }

    // 统一处理响应格式
    if (response.data && typeof response.data === 'object') {
      return response
    }

    // 包装非标准响应
    return {
      ...response,
      data: {
        success: true,
        data: response.data,
      },
    }
  },
  (error: AxiosError<ApiError>) => {
    const { response, request, message } = error

    if (response) {
      // 服务器响应了错误状态码
      const { status, data } = response
      const errorMessage = data?.message || `HTTP ${status} Error`

      // 根据状态码处理不同错误
      switch (status) {
        case 401:
          ElMessage.error('认证失败，请重新登录')
          // 清除 token 并跳转到登录页
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 422:
          // 表单验证错误
          if (data?.details && Array.isArray(data.details)) {
            data.details.forEach((detail: any) => {
              ElMessage.error(`${detail.field}: ${detail.message}`)
            })
          } else {
            ElMessage.error(errorMessage)
          }
          break
        case 429:
          ElMessage.error('请求过于频繁，请稍后再试')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(errorMessage)
      }

      return Promise.reject({
        ...error,
        response: {
          ...response,
          data: {
            success: false,
            message: errorMessage,
            code: status,
            ...data,
          },
        },
      })
    } else if (request) {
      // 请求已发出但没有收到响应
      ElMessage.error('网络连接失败，请检查网络设置')
      return Promise.reject({
        ...error,
        message: 'Network Error',
      })
    } else {
      // 请求配置出错
      ElMessage.error(message || '请求配置错误')
      return Promise.reject(error)
    }
  }
)

// 通用请求方法
export const request = {
  get: <T = any>(url: string, params?: any): Promise<AxiosResponse<ApiResponse<T>>> => {
    return api.get(url, { params })
  },

  post: <T = any>(url: string, data?: any): Promise<AxiosResponse<ApiResponse<T>>> => {
    return api.post(url, data)
  },

  put: <T = any>(url: string, data?: any): Promise<AxiosResponse<ApiResponse<T>>> => {
    return api.put(url, data)
  },

  patch: <T = any>(url: string, data?: any): Promise<AxiosResponse<ApiResponse<T>>> => {
    return api.patch(url, data)
  },

  delete: <T = any>(url: string): Promise<AxiosResponse<ApiResponse<T>>> => {
    return api.delete(url)
  },

  // 文件上传
  upload: <T = any>(url: string, formData: FormData, onProgress?: (progress: number) => void): Promise<AxiosResponse<ApiResponse<T>>> => {
    return api.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      },
    })
  },

  // 下载文件
  download: (url: string, filename?: string): Promise<void> => {
    return api.get(url, {
      responseType: 'blob',
    }).then((response) => {
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    })
  },
}

export default api
