// 通用类型定义

export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
  code?: number
}

export interface PaginationParams {
  page: number
  limit: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}

// 视频相关类型
export interface Video {
  id: string
  filename: string
  originalFilename: string
  filePath: string
  fileSize: number
  duration?: number
  width?: number
  height?: number
  format?: string
  status: 'uploading' | 'processing' | 'ready' | 'error'
  createdAt: string
  updatedAt: string
}

export interface VideoUploadRequest {
  file: File
  onProgress?: (progress: number) => void
}

// 断点相关类型
export interface Breakpoint {
  id: string
  videoId: string
  timestamp: number
  label?: string
  description?: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  createdAt: string
  updatedAt: string
}

export interface CreateBreakpointRequest {
  videoId: string
  timestamp: number
  label?: string
  description?: string
}

export interface UpdateBreakpointRequest {
  timestamp?: number
  label?: string
  description?: string
}

// 任务相关类型
export interface Task {
  id: string
  videoId: string
  breakpointId?: string
  taskType: 'frame_extraction' | 'sketch_generation' | 'batch_processing'
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled'
  progress: number
  resultData?: any
  errorMessage?: string
  startedAt?: string
  completedAt?: string
  createdAt: string
  updatedAt: string
}

export interface CreateTaskRequest {
  videoId: string
  breakpointIds?: string[]
  taskType: 'frame_extraction' | 'sketch_generation' | 'batch_processing'
}

// 生成结果相关类型
export interface GenerationResult {
  id: string
  taskId: string
  breakpointId?: string
  originalFramePath?: string
  sketchPath?: string
  thumbnailPath?: string
  metadata?: Record<string, any>
  fileSize?: number
  processingTime?: number
  createdAt: string
}

// 系统配置相关类型
export interface SystemConfig {
  id: string
  configKey: string
  configValue: string
  description?: string
  createdAt: string
  updatedAt: string
}

// 用户会话相关类型
export interface UserSession {
  id: string
  sessionToken: string
  userData: Record<string, any>
  expiresAt: string
  createdAt: string
}

// 组件 Props 类型
export interface VideoPlayerProps {
  src: string
  poster?: string
  width?: number | string
  height?: number | string
  autoplay?: boolean
  controls?: boolean
  muted?: boolean
  loop?: boolean
  playbackRate?: number
  volume?: number
}

export interface BreakpointMarkerProps {
  videoId: string
  duration: number
  breakpoints: Breakpoint[]
  currentTime: number
  onBreakpointAdd: (timestamp: number) => void
  onBreakpointUpdate: (breakpoint: Breakpoint) => void
  onBreakpointDelete: (breakpointId: string) => void
  onBreakpointSelect: (breakpoint: Breakpoint) => void
}

export interface UploadProgressProps {
  percentage: number
  status: 'uploading' | 'success' | 'error'
  message?: string
}

// 事件类型
export interface VideoPlayerEvents {
  timeupdate: (currentTime: number) => void
  loadedmetadata: (metadata: { duration: number; width: number; height: number }) => void
  play: () => void
  pause: () => void
  ended: () => void
  error: (error: Error) => void
}

export interface BreakpointEvents {
  add: (breakpoint: Breakpoint) => void
  update: (breakpoint: Breakpoint) => void
  delete: (breakpointId: string) => void
  select: (breakpoint: Breakpoint) => void
}

// 错误类型
export interface ApiError {
  code: number
  message: string
  details?: any
}

export interface ValidationError {
  field: string
  message: string
  value?: any
}

// WebSocket 消息类型
export interface WebSocketMessage {
  type: 'task_progress' | 'task_completed' | 'task_failed' | 'notification'
  data: any
  timestamp: string
}

export interface TaskProgressMessage {
  taskId: string
  progress: number
  status: Task['status']
  message?: string
}

// 文件上传相关类型
export interface FileUploadOptions {
  accept?: string
  multiple?: boolean
  maxSize?: number
  autoUpload?: boolean
  withCredentials?: boolean
  headers?: Record<string, string>
  data?: Record<string, any>
}

export interface UploadFile {
  uid: string
  name: string
  size: number
  type: string
  status: 'ready' | 'uploading' | 'success' | 'error'
  percentage: number
  response?: any
  url?: string
  raw?: File
}

// 主题相关类型
export interface ThemeConfig {
  primaryColor: string
  secondaryColor: string
  backgroundColor: string
  textColor: string
  borderColor: string
  successColor: string
  warningColor: string
  errorColor: string
  infoColor: string
}

// 工具类型
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}
