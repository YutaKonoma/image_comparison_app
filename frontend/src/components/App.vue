<!-- frontend-vue/src/App.vue -->
<script setup>
import { ref } from 'vue'
import axios from 'axios'

// LaravelのURL（.env等で管理するのが理想）
const API_BASE_URL = 'http://localhost:8080/api'

const folderPath = ref('/data') // デフォルトパス
const threshold = ref(8)
const results = ref([])
const isLoading = ref(false)
const message = ref('')

const scanImages = async () => {
  isLoading.value = true
  results.value = []
  message.value = 'スキャン中...（時間がかかる場合があります）'

  try {
    const response = await axios.post(`${API_BASE_URL}/scan`, {
      path: folderPath.value,
      threshold: threshold.value
    })
    results.value = response.data.data
    message.value = results.value.length > 0 ? `${results.value.length}件見つかりました` : '重複は見つかりませんでした'
  } catch (error) {
    message.value = 'エラーが発生しました'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

// 画像を表示するためのURL生成（Laravel経由）
const getImageUrl = (path) => {
  return `${API_BASE_URL}/image/view?path=${encodeURIComponent(path)}`
}

const deleteImage = async (path, index, pairIndex) => {
  if (!confirm('この画像を削除してもよろしいですか？')) return

  try {
    await axios.post(`${API_BASE_URL}/image/delete`, { path })
    alert('削除しました')
    // 画面から消す処理（簡易的）
    results.value.splice(pairIndex, 1)
  } catch (error) {
    alert('削除に失敗しました')
  }
}
</script>

<template>
  <div class="app-container">
    <header>
      <h1>🖼 Image Cleaner Pro</h1>
    </header>

    <main>
      <!-- 設定エリア -->
      <section class="controls">
        <div class="input-group">
          <label>フォルダパス</label>
          <input v-model="folderPath" type="text" placeholder="/data/my_images" />
        </div>
        <div class="input-group">
          <label>類似度しきい値: {{ threshold }}</label>
          <input v-model="threshold" type="range" min="0" max="32" />
        </div>
        <button @click="scanImages" :disabled="isLoading">
          {{ isLoading ? '分析中...' : 'スキャン開始' }}
        </button>
      </section>

      <div class="status-bar">{{ message }}</div>

      <!-- 結果表示エリア -->
      <section class="results-grid">
        <div v-for="(pair, pIdx) in results" :key="pIdx" class="pair-card">
          <div class="pair-container">
            <div v-for="(img_path, idx) in pair" :key="idx" class="image-item">
              <div class="img-wrapper">
                <img :src="getImageUrl(img_path)" alt="preview" />
              </div>
              <p class="file-name">{{ img_path.split('/').pop() }}</p>
              <div class="actions">
                <button class="btn-delete" @click="deleteImage(img_path, idx, pIdx)">🗑 削除</button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.app-container { max-width: 1200px; margin: 0 auto; padding: 2rem; font-family: sans-serif; background: #f8f9fa; min-height: 100vh; }
header h1 { color: #333; text-align: center; margin-bottom: 2rem; }

.controls { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: flex; gap: 1.5rem; align-items: flex-end; margin-bottom: 2rem; }
.input-group { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
input[type="text"] { padding: 0.6rem; border: 1px solid #ddd; border-radius: 6px; }
button { padding: 0.7rem 1.5rem; background: #007aff; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
button:disabled { background: #ccc; }

.status-bar { margin-bottom: 1rem; color: #666; font-weight: bold; }

.results-grid { display: flex; flex-direction: column; gap: 1.5rem; }
.pair-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #eee; }
.pair-container { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }

.image-item { text-align: center; }
.img-wrapper { height: 250px; display: flex; align-items: center; justify-content: center; background: #f0f0f0; border-radius: 8px; overflow: hidden; }
img { max-width: 100%; max-height: 100%; object-fit: contain; }
.file-name { font-size: 0.8rem; color: #777; margin: 0.5rem 0; word-break: break-all; }

.btn-delete { background: #ff3b30; font-size: 0.8rem; padding: 0.4rem 1rem; }
</style>
