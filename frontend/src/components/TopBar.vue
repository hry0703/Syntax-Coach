<template>
  <header class="topbar">
    <RouterLink to="/" class="brand">
      <div class="brand-mark">S</div>
      <div class="brand-name">Syntax <span>Coach</span></div>
    </RouterLink>

    <div v-if="sceneLabel" class="scene-pill"><i /> {{ sceneLabel }}</div>
    <nav v-else class="nav-links">
      <RouterLink to="/" exact-active-class="router-link-active">选场景</RouterLink>
      <RouterLink to="/mistakes">错题本</RouterLink>
      <RouterLink to="/review">今日复习</RouterLink>
      <RouterLink to="/history">历史</RouterLink>
      <RouterLink to="/settings">设置</RouterLink>
    </nav>

    <div class="top-actions">
      <button v-if="showEndSession" type="button" class="btn" @click="emit('endSession')">
        结束本轮
      </button>
      <RouterLink v-if="showReviewCta" to="/review" class="btn primary">今日复习</RouterLink>
    </div>
  </header>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    sceneLabel?: string
    showReviewCta?: boolean
    showEndSession?: boolean
  }>(),
  {
    showReviewCta: true,
    showEndSession: false,
  },
)

const emit = defineEmits<{
  endSession: []
}>()
</script>
