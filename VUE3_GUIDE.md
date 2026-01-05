# Vue3 前端开发实战指南 - DoodleSketchAI 项目

## 📚 目录
1. [Vue3 核心概念回顾](#vue3-核心概念回顾)
2. [项目结构深度解析](#项目结构深度解析)
3. [核心功能实现指南](#核心功能实现指南)
4. [实战开发步骤](#实战开发步骤)
5. [最佳实践与技巧](#最佳实践与技巧)

## Vue3 核心概念回顾

### 🎯 Composition API 核心思想

Vue3 的 Composition API 是一种更灵活、更类型友好的组件逻辑组织方式：

```typescript
// 传统 Options API (Vue2)
export default {
  data() {
    return { count: 0 }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}

// Composition API (Vue3)
<script setup lang="ts">
const count = ref(0)

const increment = () => {
  count.value++
}
</script>
```

**核心概念**：
- `ref()` - 创建响应式基础类型
- `reactive()` - 创建响应式对象
- `computed()` - 创建计算属性
- `watch()` - 监听响应式变化
- `<script setup>` - 更简洁的语法糖

### 🔄 响应式系统详解

```typescript
// ref - 用于基础类型
const message = ref('Hello Vue3')
// 使用：message.value

// reactive - 用于对象
const user = reactive({
  name: 'John',
  age: 25
})
// 使用：user.name

// computed - 计算属性
const doubleAge = computed(() => user.age * 2)

// watch - 监听变化
watch(user.age, (newAge, oldAge) => {
  console.log(`Age changed from ${oldAge} to ${newAge}`)
})
```

## 项目结构深度解析

### 📁 当前项目结构

```
frontend/src/
├── api/           # API 接口封装
├── assets/        # 静态资源
│   └── styles/  # 全局样式
├── components/    # 可复用组件
├── router/        # 路由配置
├── stores/        # 状态管理 (Pinia)
├── types/         # TypeScript 类型定义
├── utils/         # 工具函数
├── views/         # 页面组件
├── App.vue        # 根组件
└── main.ts        # 应用入口
```

### 🎨 样式系统架构

```scss
// assets/styles/main.scss
@import './variables.scss';    // 变量定义
@import './mixins.scss';       // 混入

// 组件内样式
<style lang="scss" scoped>
.video-player {
  // scoped 确保样式只作用于当前组件
}
</style>
```

## 核心功能实现指南

### 🎥 功能一：视频上传组件

让我们实现一个视频上传组件：

<write_to_file>
<path>frontend/src/components/VideoUpload.vue</path>
<content>
<template>
  <div class="video-upload">
    <el-upload
      class="upload-dragger"
      drag
      :action="uploadUrl"
      :before-upload="beforeUpload"
      :on-progress="onProgress"
      :on-success="onSuccess"
      :on-error="onError"
      :show-file-list="false"
      accept="video/*"
      :limit="1"
    >
      <div v-if="!uploading" class="upload-content">
        <el-icon class="upload-icon"><upload-filled /></el-icon>
        <div class="upload-text">
          <h3>上传视频文件</h3>
          <p>点击或拖拽视频文件到此处</p>
          <p class="upload-hint">支持 MP4, AVI, MOV 等格式，最大 100MB</p>
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
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

// Props 定义
interface Props {
  modelValue?: boolean  // v-model 绑定
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false
})

// Emits 定义
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'upload-success': [response: any]
  'upload-error': [error: any]
}>()

// 响应式数据
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadUrl = '/api/videos/upload'

// 更新 v-model
const updateModelValue = (value: boolean) => {
  emit('update:modelValue', value)
}

// 文件上传前检查
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
  updateModelValue(true)
  return true
}

// 上传进度
const onProgress = (event: any) => {
  uploadProgress.value = Math.round(event.percent)
}

// 上传成功
const onSuccess = (response: any, file: File) => {
  uploading.value = false
  uploadProgress.value = 0
  updateModelValue(false)
  
  if (response.success) {
    ElMessage.success('视频上传成功！')
    emit('upload-success', response.data)
  } else {
    ElMessage.error(response.message || '上传失败')
    emit('upload-error', response)
  }
}

// 上传失败
const onError = (error: any, file: File) => {
  uploading.value = false
  uploadProgress.value = 0
  updateModelValue(false)
  
  ElMessage.error('上传失败：' + error.message)
  emit('upload-error', error)
}
</script>

<style lang="scss" scoped>
.video-upload {
  .upload-dragger {
    width: 100%;
    border: 2px dashed #d9d9d9;
    border-radius: 8px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;

    &:hover {
      border-color: #409eff;
      background-color: #f5f7ff;
    }
  }

  .upload-content,
  .uploading-content {
    padding: 60px 20px;
    text-align: center;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .upload-icon {
    font-size: 48px;
    color: #c0c4cc;
    margin-bottom: 20px;
  }

  .upload-text {
    h3 {
      margin: 0 0 10px 0;
      font-size: 18px;
      color: #303133;
    }

    p {
      margin: 5px 0;
      color: #606266;
      font-size: 14px;
    }

    .upload-hint {
      font-size: 12px;
      color: #909399;
    }
  }

  .uploading-text {
    margin-top: 16px;
    color: #409eff;
    font-size: 16px;
    font-weight: 500;
  }
}
</style>
