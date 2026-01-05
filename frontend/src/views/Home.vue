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
        <!-- 跳转到编辑页面按钮 -->
        <section class="upload-section">
          <div class="upload-container">
            <div class="jump-button-container">
              <el-button 
                class="jump-button" 
                type="primary" 
                size="large"
                @click="goToVideoEditor"
              >
                <el-icon><video-play /></el-icon>
                <span>进入视频编辑页面</span>
              </el-button>
              <p class="jump-hint">点击进入视频编辑页面，上传并处理您的视频</p>
            </div>
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
import { VideoPlay, Timer, Brush, Download } from '@element-plus/icons-vue'
import type { Video } from '@/types'

const router = useRouter()

// 响应式数据
const showUploadDialog = ref(false)
const recentVideos = ref<Video[]>([])

// 生命周期
onMounted(() => {
  loadRecentVideos()
})

// 方法
const goToVideoEditor = () => {
  router.push('/video/editor')
}

const onVideoUploadSuccess = (response: any) => {
  ElMessage.success('视频上传成功')
  // 跳转到视频编辑页面
  router.push(`/video/${response.data.id}`)
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

  .jump-button-container {
    text-align: center;
    padding: 40px 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;

    &:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.4);
      transform: translateY(-5px);
    }

    .jump-button {
      padding: 20px 40px;
      font-size: 1.2rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);

      .el-icon {
        margin-right: 10px;
        font-size: 1.5rem;
      }

      span {
        font-weight: 600;
      }

      &:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        transform: scale(1.05);
      }
    }

    .jump-hint {
      margin-top: 20px;
      color: rgba(255, 255, 255, 0.8);
      font-size: 0.9rem;
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
