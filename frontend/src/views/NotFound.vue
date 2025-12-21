<template>
  <div class="not-found">
    <div class="container">
      <h1>404</h1>
      <p>页面未找到</p>
      <div class="actions">
        <el-button type="primary" @click="$router.push('/')">
          返回首页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 页面组件
</script>

<style lang="scss" scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  .container {
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 60px 40px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);

    h1 {
      font-size: 6rem;
      margin-bottom: 20px;
      color: white;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    p {
      font-size: 1.2rem;
      margin-bottom: 30px;
      color: rgba(255, 255, 255, 0.8);
    }

    .actions {
      .el-button {
        padding: 12px 30px;
        font-size: 16px;
      }
    }
  }
}
</style>
