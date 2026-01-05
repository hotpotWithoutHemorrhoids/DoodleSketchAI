<template>
    <div class="  ">
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
                    >
                    <p class="uploading-text">上传中....{{ uploadProgress }}%</p>
                </el-progress>
            </div>
        </el-upload>
    </div>
</template>


<script setup lang="ts">
    import { ref } from 'vue';
    import {ElMessage} from 'element-plus'
    import { UploadFilled } from '@element-plus/icons-vue';
    import { useRouter } from 'vue-router';

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

    const router = useRouter();
    
    const uploading = ref(false)
    const uploadProgress = ref(0)
    const uploadUrl = '/api/v1/upload/video'
    
    // 更新 v-model
    const updateModelValue = (value: boolean)=>{
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
  uploading.value = false;
  uploadProgress.value = 0;
  updateModelValue(false);

  if (response?.success) {
    ElMessage.success('视频上传成功！');
    emit('upload-success', response.data);

    // ✅ 创建本地 Blob URL（用于预览）
    const url = URL.createObjectURL(file);
    videoBlobUrl.value = url; // 如果你在 setup 中声明了这个 ref

    // 跳转到播放页，并通过 router state 传递 blob URL
    router.push({
      path: `/video/${response.data.filename}`,
      state: {
        blobUrl: url,
        // 注意：File 对象无法被 history.state 序列化，所以不要传 originalFile
        // 如果后续需要，可通过其他方式（如 Pinia）临时保存
      }
    });
  } else {
    ElMessage.error(response?.message || '上传失败');
    emit('upload-error', response);
  }
};

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
