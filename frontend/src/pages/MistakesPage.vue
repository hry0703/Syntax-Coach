<template>
  <div class="page-shell">
    <div class="frame">
      <TopBar />
      <div class="placeholder">
        <h1>错题本</h1>
        <p>按语法点沉淀薄弱项。当前为骨架：列表来自后端内存 stub。</p>
      </div>
      <div v-if="loading" class="placeholder">加载中…</div>
      <div v-else-if="error" class="placeholder"><p>{{ error }}</p></div>
      <div v-else-if="!mistakes.length" class="placeholder">
        <p>还没有错题。去对话页点「加入薄弱语法点」试试。</p>
      </div>
      <div v-else class="mistake-list">
        <div v-for="item in mistakes" :key="item.id" class="mistake-item">
          <div class="title">{{ item.grammar_point_id }}</div>
          <div class="muted">原句：{{ item.original }}</div>
          <div class="muted">改写：{{ item.corrected }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import TopBar from '../components/TopBar.vue'
import { fetchMistakes } from '../api/endpoints'
import type { Mistake } from '../types'

const mistakes = ref<Mistake[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    mistakes.value = await fetchMistakes()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
})
</script>
