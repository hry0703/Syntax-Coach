<template>
  <div class="page-shell">
    <div class="frame">
      <TopBar />
      <div class="placeholder">
        <h1>设置</h1>
        <p>水平、目标与解析详细度（骨架可读写后端内存档案）。</p>
      </div>
      <form class="settings-form" @submit.prevent="save">
        <label>
          水平
          <select v-model="profile.level">
            <option value="A2">A2</option>
            <option value="B1">B1</option>
            <option value="B2">B2</option>
          </select>
        </label>
        <label>
          目标
          <select v-model="profile.goal">
            <option value="speaking">口语</option>
            <option value="business">商务</option>
            <option value="exam">考试</option>
          </select>
        </label>
        <label>
          纠错严格度
          <select v-model="profile.correction_strictness">
            <option value="light">轻度</option>
            <option value="standard">标准</option>
            <option value="strict">严格</option>
          </select>
        </label>
        <label>
          解析详细度
          <select v-model="profile.explanation_detail">
            <option value="brief">简略</option>
            <option value="standard">标准</option>
            <option value="detailed">详细</option>
          </select>
        </label>
        <button type="submit" class="btn primary" :disabled="saving">
          {{ saving ? '保存中…' : '保存' }}
        </button>
        <p v-if="message" class="footnote">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import TopBar from '../components/TopBar.vue'
import { fetchProfile, updateProfile } from '../api/endpoints'
import type { UserProfile } from '../types'

const profile = ref<UserProfile>({
  level: 'B1',
  goal: 'speaking',
  correction_strictness: 'standard',
  explanation_detail: 'standard',
  show_terms: false,
})
const saving = ref(false)
const message = ref('')

onMounted(async () => {
  try {
    profile.value = await fetchProfile()
  } catch {
    message.value = '未能读取档案，显示本地默认值'
  }
})

async function save() {
  saving.value = true
  message.value = ''
  try {
    profile.value = await updateProfile(profile.value)
    message.value = '已保存'
  } catch {
    message.value = '保存失败：请确认后端已启动'
  } finally {
    saving.value = false
  }
}
</script>
