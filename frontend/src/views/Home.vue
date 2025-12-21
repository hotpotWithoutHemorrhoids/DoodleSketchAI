<template>
  <div class="home">
    <div class="container">
      <!-- 头部 -->
      <header class="header">
        <div class="logo">
          <h1>DoodleSketchAI</h1>
          <p class="subtitle">AI驱动的视频简笔画生成工具</p>
        </div>
      </header>

      <!-- 主要内容 -->
      <main class="main">
        <!-- 上传区域 -->
        <section class="upload-section">
          <div class="upload-container">
            <el-upload
              class="video-uploader"
              drag
              :action="uploadUrl"
              :before-upload="beforeUpload"
              :on-progress="onUploadProgress"
              :on-success="onUploadSuccess"
              :on-error="onUploadError"
              :file-list="fileList"
              :auto-upload="true"
              :show-file-list="false"
              accept="video/*"
            >
              <div v-if="!uploading" class="upload-content">
                <el-icon class="upload-icon"><upload-filled /></el-icon>
                <div class="upload-text">
                  <p>点击或拖拽视频文件到此处上传</p>
                  <p class="upload-hint">支持 MP4, AVI, MOV, WMV, FLV, WebM 格式</p>
                  <p class="upload-hint">文件大小不超过 100MB</p>
                </div>
              </div>
              <div v-else class="uploading-content">
                <el-progress
                  type="circle"
                  :percentage="uploadProgress"
                  :width="80"
                  :stroke-width="6"
                />
                <p class="uploading-text">上传中... {{ uploadProgress }}%</p>
              </div>
            </el-upload>
          </div>
        </section>

        <!-- 功能介绍 -->
        <section class="features-section">
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><video-play /></el-icon>
              </div>
              <h3>视频上传</h3>
              <p>支持多种视频格式，快速上传和处理</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><timer /></el-icon>
              </div>
              <h3>智能断点</h3>
              <p>可视化时间轴，精确标记关键帧</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><brush /></el-icon>
              </div>
              <h3>AI生成</h3>
              <p>基于深度学习的简笔画风格化</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon><download /></el-icon>
              </div>
              <h3>结果下载</h3>
              <p>高质量结果图片，支持批量下载</p>
            </div>
          </div>
        </section>

        <!-- 最近项目 -->
        <section v-if="recentVideos.length > 0" class="recent-section">
          <h2>最近项目</h2>
          <div class="recent-grid">
            <div
              v-for="video in recentVideos"
              :key="video.id"
              class="video-card"
              @click="openVideo(video.id)"
            >
              <div class="video-thumbnail">
                <img
                  v-if="video.thumbnail"
                  :src="video.thumbnail"
                  :alt="video.originalFilename"
                />
                <div v-else class="thumbnail-placeholder">
                  <el-icon><video-play /></el-icon>
                </div>
              </div>
              <div class="video-info">
                <h4>{{ video.originalFilename }}</h4>
                <p class="video-meta">
                  {{ formatFileSize(video.fileSize) }} · {{ formatDate(video.createdAt) }}
                </p>
                <div class="video-status">
                  <el-tag
                    :type="getStatusType(video.status)"
                    size="small"
                  >
                    {{ getStatusText(video.status) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled, VideoPlay, Timer, Brush, Download } from '@element-plus/icons-vue'
import type { Video, UploadFile } from '@/types'

const router = useRouter()

// 响应式数据
const uploadUrl = '/api/videos/upload'
const uploading = ref(false)
const uploadProgress = ref(0)
const fileList = ref<UploadFile[]>([])
const recentVideos = ref<Video[]>([])

// 生命周期
onMounted(() => {
  loadRecentVideos()
})

// 方法
const beforeUpload = (file: File) => {
  // 文件类型检查
  const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/flv', 'video/webm']
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('不支持的文件格式，请上传视频文件')
    return false
  }

  // 文件大小检查 (100MB)
  const maxSize = 100 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 100MB')
    return false
  }

  uploading.value = true
  uploadProgress.value = 0
  return true
}

const onUploadProgress = (event: any) => {
  uploadProgress.value = Math.round(event.percent)
}

const onUploadSuccess = (response: any) => {
  uploading.value = false
  uploadProgress.value = 0
  
  if (response.success) {
    ElMessage.success('视频上传成功')
    // 跳转到视频编辑页面
    router.push(`/video/${response.data.id}`)
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

const onUploadError = (error: any) => {
  uploading.value = false
  uploadProgress.value = 0
  ElMessage.error('上传失败，请重试')
}

const loadRecentVideos = async () => {
  try {
    // 这里应该调用 API 获取最近的视频列表
    // const response = await request.get<Video[]>('/videos/recent')
    // recentVideos.value = response.data.data
    
    // 模拟数据
    recentVideos.value = []
  } catch (error) {
    console.error('Failed to load recent videos:', error)
  }
}

const openVideo = (videoId: string) => {
  router.push(`/video/${videoId}`)
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    uploading: 'warning',
    processing: 'info',
    ready: 'success',
    error: 'danger',
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    uploading: '上传中',
    processing: '处理中',
    ready: '已完成',
    error: '错误',
  }
  return statusMap[status] || '未知'
}
</script>

<style lang="scss" scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header {
  text-align: center;
  padding: 60px 0 40px;
  color: white;

  .logo {
    h1 {
      font-size: 3rem;
      margin-bottom: 10px;
      font-weight: 700;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .subtitle {
      font-size: 1.2rem;
      opacity: 0.9;
      margin: 0;
    }
  }
}

.main {
  padding-bottom: 60px;
}

.upload-section {
  margin-bottom: 60px;

  .upload-container {
    max-width: 600px;
    margin: 0 auto;
  }

  .video-uploader {
    width: 100%;

    :deep(.el-upload) {
      width: 100%;
      border: 2px dashed rgba(255, 255, 255, 0.3);
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      transition: all 0.3s ease;

      &:hover {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.15);
      }
    }

    :deep(.el-upload-dragger) {
      width: 100%;
      height: 200px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: transparent;
      border: none;
    }

    .upload-content {
      text-align: center;
      color: white;

      .upload-icon {
        font-size: 48px;
        margin-bottom: 20px;
        opacity: 0.8;
      }

      .upload-text {
        p {
          margin: 8px 0;
          font-size: 16px;
        }

        .upload-hint {
          font-size: 14px;
          opacity: 0.7;
        }
      }
    }

    .uploading-content {
      text-align: center;
      color: white;

      .uploading-text {
        margin-top: 16px;
        font-size: 16px;
      }
    }
  }
}

.features-section {
  margin-bottom: 60px;

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
  }

  .feature-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    color: white;
    transition: transform 0.3s ease, background 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      background: rgba(255, 255, 255, 0.15);
    }

    .feature-icon {
      font-size: 48px;
      margin-bottom: 20px;
      opacity: 0.9;
    }

    h3 {
      font-size: 1.3rem;
      margin-bottom: 10px;
    }

    p {
      opacity: 0.8;
      line-height: 1.6;
    }
  }
}

.recent-section {
  h2 {
    color: white;
    font-size: 2rem;
    margin-bottom: 30px;
    text-align: center;
  }

  .recent-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }

  .video-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s ease, background 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      background: rgba(255, 255, 255, 0.15);
    }

    .video-thumbnail {
      height: 180px;
      background: rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .thumbnail-placeholder {
        font-size: 48px;
        color: rgba(255, 255, 255, 0.6);
      }
    }

    .video-info {
      padding: 20px;

      h4 {
        color: white;
        margin-bottom: 8px;
        font-size: 1.1rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .video-meta {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-bottom: 12px;
      }

      .video-status {
        display: flex;
        align-items: center;
      }
    }
  }
}

@media (max-width: 768px) {
  .header .logo h1 {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .recent-grid {
    grid-template-columns: 1fr;
  }
}
</style>
