<template>
  <aside class="panel">
    <div class="panel-label">
      <h2>Grammar Card</h2>
      <span v-if="card" class="badge">{{ errorCount }} 处明确错误</span>
    </div>

    <div v-if="!card" class="empty-card">
      发送一句英文后，这里会显示结构化语法解析卡片。
    </div>

    <article v-else class="card">
      <div class="point-row">
        <h3>{{ card.title_zh }}</h3>
        <span class="level">CEFR {{ card.cefr }}</span>
      </div>

      <div class="sentence-box">
        <div class="caption">原句 · 错误跨度高亮</div>
        <p
          class="sentence"
          v-html="highlightBySpans(card.original, card.error_spans, 'mark')"
        />
      </div>

      <div class="compare">
        <div class="row bad">
          <div class="tag">错误</div>
          <div v-html="badHtml" />
        </div>
        <div class="row good">
          <div class="tag">正确</div>
          <div>{{ card.corrected }}</div>
        </div>
      </div>

      <div class="rule">
        <h4>为什么错</h4>
        <p>{{ card.rule_zh }}</p>
      </div>

      <div class="examples">
        <h4>同类正确例句</h4>
        <ul>
          <li v-for="ex in card.examples" :key="ex">{{ ex }}</li>
        </ul>
      </div>

      <div class="actions">
        <button type="button" class="btn">下一条建议说法</button>
        <button type="button" class="btn primary" @click="emit('addWeakPoint')">
          加入薄弱语法点
        </button>
      </div>
    </article>

    <p class="footnote">
      骨架阶段卡片来自后端 stub；后续由 LangChain + LangGraph Agent 生成同结构 JSON。
    </p>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { highlightBySpans } from '../utils/highlight'
import type { GrammarCard } from '../types'

const props = defineProps<{
  card: GrammarCard | null
}>()

const emit = defineEmits<{
  addWeakPoint: []
}>()

const errorCount = computed(() => {
  if (!props.card) return 0
  return props.card.error_spans.length || (props.card.severity === 'error' ? 1 : 0)
})

const badHtml = computed(() => {
  if (!props.card) return ''
  const span = props.card.error_spans[0]
  if (!span) return props.card.original
  const { original } = props.card
  return (
    escape(original.slice(0, span.start)) +
    `<span class="strike">${escape(original.slice(span.start, span.end))}</span>` +
    escape(original.slice(span.end))
  )
})

function escape(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
}
</script>
