<template>
  <div class="video-player">
    <div class="video-container">
      <video
        ref="videoRef"
        class="video-js vjs-default-skin"
        controls
        preload="metadata"
        :poster="poster"
        data-setup="{}"
      >
        <source :src="src" :type="getVideoType(src)" />
      </video>
      
      <!-- 自定义控制层 -->
      <div class="video-controls" v-if="showCustomControls">
        <div class="progress-container">
          <div class="progress-bar" @click="seekVideo">
            <div 
              class="progress-filled" 
              :style="{ width: progressPercentage + '%' }"
            ></div>
            <div 
              class="progress-handle" 
              :style="{ left: progressPercentage + '%' }"
            ></div>
          </div>
          <div class="time-display">
            {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
          </div>
        </div>
        
        <div class="control-buttons">
          <button @click="togglePlay" class="control-btn">
            <el-icon>
              <video-pause v-if="!isPlaying" />
              <video-play v-else />
            </el-icon>
          </button>
          
          <button @click="toggleMute" class="control-btn">
            <el-icon>
              <mute v-if="!isMuted" />
              <microphone v-else />
            </el-icon>
          </button>
          
          <div class="volume-control">
            <input
              type="range"
              v-model="volume"
              min="0"
              max="1"
              step="0.1"
              @input="updateVolume"
              class="volume-slider"
            />
          </div>
        </div>
      </div>
      
      <!-- 断点标记 -->
      <div class="breakpoint-markers" v-if="breakpoints.length > 0">
        <div
          v-for="breakpoint in breakpoints"
          :key="breakpoint.id"
          class="breakpoint-marker"
          :style="{ left: (breakpoint.timestamp / duration * 100) + '%' }"
          @click="seekToTime(breakpoint.timestamp)"
          :title="breakpoint.label || '断点 ' + breakpoint.timestamp"
        >
          <div class="breakpoint-dot"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { VideoPlay, VideoPause, Mute, Microphone } from '@element-plus/icons-vue'

// Props 定义
interface Props {
  src: string
  poster?: string
  autoplay?: boolean
  showCustomControls?: boolean
  breakpoints?: Array<{
    id: string
    timestamp: number
    label?: string
  }>
}

const props = withDefaults(defineProps<Props>(), {
  autoplay: false,
  showCustomControls: false,
  breakpoints: () => []
})

// Emits 定义
const emit = defineEmits<{
  timeupdate: [currentTime: number]
  loadedmetadata: [metadata: { duration: number; width: number; height: number }]
  breakpointClick: [breakpoint: any]
}>()

// 响应式数据
const videoRef = ref<HTMLVideoElement>()
const isPlaying = ref(false)
const isMuted = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(1)
const progressPercentage = ref(0)
let player: any = null

// 工具函数
const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

const getVideoType = (src: string): string => {
  const extension = src.split('.').pop()?.toLowerCase()
  const typeMap: Record<string, string> = {
    mp4: 'video/mp4',
    webm: 'video/webm',
    ogg: 'video/ogg',
    avi: 'video/avi',
    mov: 'video/quicktime',
    wmv: 'video/x-ms-wmv',
    flv: 'video/x-flv'
  }
  return typeMap[extension || 'mp4'] || 'video/mp4'
}

// 播放控制
const togglePlay = () => {
  if (!player) return
  
  if (isPlaying.value) {
    player.pause()
  } else {
    player.play()
  }
}

const toggleMute = () => {
  if (!player) return
  
  player.muted(!player.muted())
  isMuted.value = player.muted()
}

const updateVolume = () => {
  if (!player) return
  
  player.volume(volume.value)
}

const seekVideo = (event: MouseEvent) => {
  if (!player || !duration.value) return
  
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  const clickX = event.clientX - rect.left
  const percentage = (clickX / rect.width) * 100
  const seekTime = (percentage / 100) * duration.value
  
  player.currentTime(seekTime)
}

const seekToTime = (timestamp: number) => {
  if (!player) return
  
  player.currentTime(timestamp)
  emit('breakpointClick', timestamp)
}

// 生命周期
onMounted(() => {
  if (videoRef.value) {
    // 动态导入 video.js
    import('video.js').then((videojs) => {
      player = videojs(videoRef.value, {
        controls: !props.showCustomControls,
        autoplay: props.autoplay,
        preload: 'metadata',
        fluid: true,
        responsive: true
      })

      // 事件监听
      player.on('timeupdate', () => {
        currentTime.value = player.currentTime()
        progressPercentage.value = (currentTime.value / duration.value) * 100
        emit('timeupdate', currentTime.value)
      })

      player.on('loadedmetadata', () => {
        duration.value = player.duration()
        emit('loadedmetadata', {
          duration: duration.value,
          width: player.videoWidth(),
          height: player.videoHeight()
        })
      })

      player.on('play', () => {
        isPlaying.value = true
      })

      player.on('pause', () => {
        isPlaying.value = false
      })

      player.on('volumechange', () => {
        volume.value = player.volume()
        isMuted.value = player.muted()
      })
    })
  }
})

onUnmounted(() => {
  if (player) {
    player.dispose()
    player = null
  }
})

// 监听断点变化
watch(() => props.breakpoints, () => {
  // 断点变化时可以重新渲染标记
}, { deep: true })
</script>

<style lang="scss" scoped>
.video-player {
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  position: relative;

  .video-container {
    position: relative;
    width: 100%;
  }

  .video-js {
    width: 100%;
    height: auto;
  }

  .video-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
    padding: 15px;
    display: flex;
    align-items: center;
    gap: 15px;
  }

  .progress-container {
    flex: 1;
    position: relative;
    height: 6px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
    cursor: pointer;
  }

  .progress-bar {
    position: relative;
    width: 100%;
    height: 100%;
  }

  .progress-filled {
    height: 100%;
    background: #409eff;
    border-radius: 3px;
    transition: width 0.1s ease;
  }

  .progress-handle {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 12px;
    height: 12px;
    background: #409eff;
    border-radius: 50%;
    cursor: grab;
  }

  .time-display {
    font-size: 12px;
    color: white;
    font-weight: 500;
    min-width: 100px;
    text-align: center;
  }

  .control-buttons {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .control-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    border-radius: 4px;
    padding: 8px;
    cursor: pointer;
    color: white;
    transition: background 0.2s ease;

    &:hover {
      background: rgba(255, 255, 255, 0.3);
    }
  }

  .volume-control {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .volume-slider {
    width: 80px;
    height: 4px;
    -webkit-appearance: none;
    appearance: none;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    outline: none;

    &::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 12px;
      height: 12px;
      background: #409eff;
      border-radius: 50%;
      cursor: pointer;
    }

    &::-moz-range-thumb {
      width: 12px;
      height: 12px;
      background: #409eff;
      border-radius: 50%;
      cursor: pointer;
      border: none;
    }
  }

  .breakpoint-markers {
    position: absolute;
    top: 10px;
    left: 0;
    right: 0;
    height: 20px;
    pointer-events: none;
  }

  .breakpoint-marker {
    position: absolute;
    top: 0;
    width: 2px;
    height: 100%;
    background: #e6a23c;
    cursor: pointer;
    pointer-events: all;
    transition: all 0.2s ease;

    &:hover {
      background: #f56c6c;
      transform: scaleX(2);
    }
  }

  .breakpoint-dot {
    position: absolute;
    top: -4px;
    left: -4px;
    width: 10px;
    height: 10px;
    background: #e6a23c;
    border: 2px solid white;
    border-radius: 50%;
  }
}
</style>
