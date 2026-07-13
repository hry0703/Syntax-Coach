<template>
  <div class="page-shell">
    <div class="frame">
      <TopBar :show-review-cta="false" />
      <div class="placeholder">
        <h1>今日复习</h1>
        <p>占位页。后续按薄弱语法点出改错 / 造句题，并由 Agent 点评。</p>
        <p style="margin-top: 12px">接口预留：`GET /api/review/today`、`POST /api/review/submit`</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import TopBar from '../components/TopBar.vue'
</script>
