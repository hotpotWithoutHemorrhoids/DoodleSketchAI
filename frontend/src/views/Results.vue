<template>
  <div class="results">
    <div class="container">
      <h1>生成结果</h1>
      <p>视频ID: {{ $route.params.videoId }}</p>
      <div class="placeholder">
        <p>结果页面正在开发中...</p>
        <el-button @click="$router.push('/')">返回首页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style lang="scss" scoped>
.results {
  min-height: 100vh;
  padding: 40px 20px;
  background: #f5f5f5;

  .container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    padding: 40px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    h1 {
      margin-bottom: 20px;
      color: #333;
    }

    .placeholder {
      text-align: center;
      padding: 60px 20px;
      color: #666;

      p {
        margin-bottom: 20px;
        font-size: 16px;
      }
    }
  }
}
</style>
