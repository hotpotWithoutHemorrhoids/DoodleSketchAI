<template>
  <div class="video-editor">
    <!-- 顶部导航 -->
    <div class="editor-header">
      <div class="header-left">
        <h1>视频编辑器</h1>
        <p class="subtitle">上传、编辑和处理您的视频</p>
      </div>
      <div class="header-right">
        <el-button @click="goHome" type="primary" plain>
          <el-icon><HomeFilled /></el-icon>
          返回首页
        </el-button>
        <el-button @click="goResults" type="success">
          <el-icon><View /></el-icon>
          查看生成结果
        </el-button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="editor-main">
      <!-- 左侧视频播放区域 (约占左侧的一半还多一些) -->
      <div class="video-section">
        <div class="video-container">
          <div class="video-header">
            <h3>视频播放器</h3>
            <div class="video-controls">
              <el-button-group>
                <el-button @click="togglePlay" :type="isPlaying ? 'info' : 'primary'">
                  <el-icon v-if="isPlaying"><VideoPause /></el-icon>
                  <el-icon v-else><VideoPlay /></el-icon>
                  {{ isPlaying ? '暂停' : '播放' }}
                </el-button>
                <el-button @click="uploadVideo" type="success">
                  <el-icon><UploadFilled /></el-icon>
                  上传视频
                </el-button>
                <el-button @click="takeSnapshot" type="warning">
                  <el-icon><CameraFilled /></el-icon>
                  截图
                </el-button>
              </el-button-group>
            </div>
          </div>
          
          <div class="video-player-wrapper">
            <VideoPlayer
              ref="videoPlayerRef"
              :src="videoSrc"
              :controls="true"
              :autoplay="false"
              width="100%"
              height="100%"
              @play="onPlay"
              @pause="onPause"
              @timeupdate="onTimeUpdate"
            />
          </div>

          <!-- 视频信息 -->
          <div class="video-info">
            <div class="info-item">
              <span class="label">当前视频:</span>
              <span class="value">{{ currentVideoName || '未选择视频' }}</span>
            </div>
            <div class="info-item">
              <span class="label">时长:</span>
              <span class="value">{{ formatDuration(videoDuration) }}</span>
            </div>
            <div class="info-item">
              <span class="label">当前时间:</span>
              <span class="value">{{ formatDuration(currentTime) }}</span>
            </div>
            <div class="info-item">
              <span class="label">分辨率:</span>
              <span class="value">{{ videoResolution }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧列表框区域 (留出，先实现视频播放功能) -->
      <div class="list-section">
        <div class="list-container">
          <div class="list-header">
            <h3>视频列表</h3>
            <el-button @click="refreshVideoList" type="text" size="small">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
          
          <div class="list-content">
            <div v-if="videoList.length === 0" class="empty-state">
              <el-icon><FolderOpened /></el-icon>
              <p>暂无视频文件</p>
              <p class="hint">上传视频后，文件将显示在这里</p>
            </div>
            
            <div
              v-for="(video, index) in videoList"
              :key="index"
              class="list-item"
              :class="{ selected: selectedVideoIndex === index }"
              @click="selectVideo(index)"
            >
              <div class="item-thumbnail">
                <div class="thumbnail-placeholder">
                  <el-icon><VideoPlay /></el-icon>
                </div>
              </div>
              <div class="item-info">
                <div class="item-name">{{ video.name }}</div>
                <div class="item-meta">
                  <span class="item-size">{{ video.size }}</span>
                  <span class="item-duration">{{ video.duration }}</span>
                </div>
                <div class="item-status">
                  <el-tag :type="getVideoStatusType(video.status)" size="small">
                    {{ video.status }}
                  </el-tag>
                </div>
              </div>
              <div class="item-actions">
                <el-button @click.stop="playVideo(video)" type="text" size="small">
                  播放
                </el-button>
                <el-button @click.stop="deleteVideo(video)" type="text" size="small">
                  删除
                </el-button>
              </div>
            </div>
          </div>
          
          <div class="list-footer">
            <el-button @click="uploadVideo" type="primary" plain style="width: 100%;">
              <el-icon><UploadFilled /></el-icon>
              上传新视频
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  HomeFilled,
  View,
  VideoPlay,
  VideoPause,
  UploadFilled,
  CameraFilled,
  Refresh,
  FolderOpened
} from '@element-plus/icons-vue'
import VideoPlayer from '@/components/VideoPlayer.vue'

const route = useRoute()
const router = useRouter()

// 视频播放相关
const videoPlayerRef = ref()
const isPlaying = ref(false)
const currentTime = ref(0)
const videoDuration = ref(0)
const videoResolution = ref('未知')
const currentVideoName = ref('')

// 构建视频源URL
const videoSrc = computed(() => {
  const videoId = route.params.id as string
  return videoId ? `/uploads/videos/${videoId}` : ''
})

// 视频列表相关
const videoList = ref<Array<{
  id: string
  name: string
  size: string
  duration: string
  status: string
}>>([])
const selectedVideoIndex = ref(-1)

// 模拟数据
onMounted(() => {
  // 模拟一些视频文件
  videoList.value = [
    {
      id: '1',
      name: '示例视频1.mp4',
      size: '45.2 MB',
      duration: '02:30',
      status: '已上传'
    },
    {
      id: '2',
      name: '示例视频2.mov',
      size: '78.5 MB',
      duration: '01:45',
      status: '已上传'
    },
    {
      id: '3',
      name: '示例视频3.avi',
      size: '120.3 MB',
      duration: '03:20',
      status: '处理中'
    }
  ]
})

// 视频控制方法
const togglePlay = () => {
  if (videoPlayerRef.value) {
    if (isPlaying.value) {
      // 这里需要调用视频播放器的pause方法
      // 假设VideoPlayer组件有pause方法
      const player = videoPlayerRef.value
      if (player.pause) player.pause()
    } else {
      // 假设VideoPlayer组件有play方法
      const player = videoPlayerRef.value
      if (player.play) player.play()
    }
  }
}

const onPlay = () => {
  isPlaying.value = true
}

const onPause = () => {
  isPlaying.value = false
}

const onTimeUpdate = (time: number) => {
  currentTime.value = time
}

const uploadVideo = () => {
  // 这里应该实现视频上传逻辑
  ElMessage.info('视频上传功能待实现')
}

const takeSnapshot = () => {
  ElMessage.success('截图已保存')
}

// 视频列表方法
const refreshVideoList = () => {
  ElMessage.info('刷新视频列表')
}

const selectVideo = (index: number) => {
  selectedVideoIndex.value = index
  const video = videoList.value[index]
  if (video) {
    currentVideoName.value = video.name
    // 这里应该加载选中的视频
    ElMessage.info(`选中视频: ${video.name}`)
  }
}

const playVideo = (video: any) => {
  ElMessage.info(`播放视频: ${video.name}`)
  // 这里应该切换到播放选中的视频
}

const deleteVideo = (video: any) => {
  ElMessage.success(`删除视频: ${video.name}`)
  // 这里应该实现删除视频的逻辑
}

const getVideoStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    '已上传': 'success',
    '处理中': 'info',
    '失败': 'danger',
    '等待中': 'warning'
  }
  return statusMap[status] || 'info'
}

// 工具方法
const formatDuration = (seconds: number): string => {
  if (!seconds) return '00:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 导航方法
const goHome = () => {
  router.push('/')
}

const goResults = () => {
  router.push(`/results/${route.params.id || 'demo'}`)
}
</script>

<style lang="scss" scoped>
.video-editor {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  .header-left {
    h1 {
      margin: 0 0 8px 0;
      color: #303133;
      font-size: 1.8rem;
    }

    .subtitle {
      margin: 0;
      color: #909399;
      font-size: 0.9rem;
    }
  }

  .header-right {
    display: flex;
    gap: 10px;
  }
}

.editor-main {
  display: flex;
  gap: 20px;
  height: calc(100vh - 160px);

  .video-section {
    flex: 3; /* 约占左侧的一半还多一些 (60%) */
    display: flex;
    flex-direction: column;
  }

  .list-section {
    flex: 2; /* 右侧列表框区域 (40%) */
    display: flex;
    flex-direction: column;
  }
}

.video-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;

  .video-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #ebeef5;

    h3 {
      margin: 0;
      color: #303133;
      font-size: 1.2rem;
    }
  }

  .video-player-wrapper {
    flex: 1;
    min-height: 0;
    padding: 20px;
  }

  .video-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    padding: 15px 20px;
    border-top: 1px solid #ebeef5;
    background: #fafafa;

    .info-item {
      display: flex;
      align-items: center;

      .label {
        color: #606266;
        font-size: 0.9rem;
        margin-right: 8px;
        min-width: 70px;
      }

      .value {
        color: #303133;
        font-weight: 500;
        font-size: 0.9rem;
      }
    }
  }
}

.list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;

  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #ebeef5;

    h3 {
      margin: 0;
      color: #303133;
      font-size: 1.2rem;
    }
  }

  .list-content {
    flex: 1;
    overflow-y: auto;
    padding: 10px;

    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 200px;
      color: #909399;

      .el-icon {
        font-size: 48px;
        margin-bottom: 15px;
        opacity: 0.6;
      }

      p {
        margin: 5px 0;
        text-align: center;
      }

      .hint {
        font-size: 0.9rem;
        opacity: 0.7;
      }
    }

    .list-item {
      display: flex;
      align-items: center;
      padding: 12px;
      border-radius: 6px;
      cursor: pointer;
      transition: background-color 0.2s ease;
      margin-bottom: 8px;

      &:hover {
        background-color: #f5f7fa;
      }

      &.selected {
        background-color: #ecf5ff;
        border: 1px solid #409eff;
      }

      .item-thumbnail {
        width: 60px;
        height: 40px;
        background: #f0f2f5;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;

        .thumbnail-placeholder {
          color: #909399;
          font-size: 20px;
        }
      }

      .item-info {
        flex: 1;
        min-width: 0;

        .item-name {
          font-weight: 500;
          color: #303133;
          margin-bottom: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .item-meta {
          display: flex;
          gap: 10px;
          font-size: 0.8rem;
          color: #909399;

          span {
            display: inline-block;
          }
        }

        .item-status {
          margin-top: 4px;
        }
      }

      .item-actions {
        display: flex;
        gap: 5px;
        opacity: 0;
        transition: opacity 0.2s ease;

        .el-button {
          padding: 4px 8px;
          font-size: 0.8rem;
        }
      }

      &:hover .item-actions {
        opacity: 1;
      }
    }
  }

  .list-footer {
    padding: 15px 20px;
    border-top: 1px solid #ebeef5;
  }
}

@media (max-width: 1200px) {
  .editor-main {
    flex-direction: column;
    height: auto;

    .video-section,
    .list-section {
      flex: none;
      width: 100%;
      height: 500px;
      margin-bottom: 20px;
    }
  }
}
</style>
