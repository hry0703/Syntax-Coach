<template>
  <div class="page-shell">
    <div class="frame">
      <TopBar />
      <div>
        <div class="placeholder" style="padding-bottom: 8px">
          <h1>选一个场景开始练</h1>
          <p>对话是入口，语法解析是核心。聊完自动沉淀语法点，再回来专项复习。</p>
        </div>
        <ScenePicker :scenes="scenes" :loading="loading" :error="error" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import TopBar from '../components/TopBar.vue'
import ScenePicker from '../components/ScenePicker.vue'
import { fetchScenes } from '../api/endpoints'
import type { Scene } from '../types'

const scenes = ref<Scene[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    scenes.value = await fetchScenes()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
})
</script>
