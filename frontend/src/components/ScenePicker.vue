<template>
  <div v-if="loading" class="placeholder">正在加载场景…</div>
  <div v-else-if="error" class="placeholder">
    <h1>无法加载场景</h1>
    <p>{{ error }}</p>
  </div>
  <div v-else class="scene-grid">
    <button
      v-for="scene in scenes"
      :key="scene.id"
      type="button"
      class="scene-card"
      @click="openScene(scene.id)"
    >
      <div class="meta">{{ scene.level }} · {{ scene.role }}</div>
      <h3>{{ scene.title_zh }}</h3>
      <p>{{ scene.description }}</p>
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Scene } from '../types'

defineProps<{
  scenes: Scene[]
  loading: boolean
  error: string | null
}>()

const router = useRouter()

function openScene(id: string) {
  router.push(`/chat/${id}`)
}
</script>
