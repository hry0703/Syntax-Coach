<template>
  <section class="chat">
    <div class="chat-meta">
      <span>对话进行中 · 第 {{ turn }} 轮 · 对方：{{ roleName }}</span>
      <span>纠错模式：语法解析</span>
    </div>

    <div ref="messagesEl" class="messages">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="msg"
        :class="[msg.role, { active: msg.active }]"
      >
        <div class="who">{{ msg.who }}</div>
        <div
          v-if="msg.role === 'user'"
          class="bubble"
          v-html="highlightBySpans(msg.content, msg.errorSpans)"
        />
        <div v-else class="bubble">{{ msg.content }}</div>
        <div v-if="msg.active" class="hint">↗ 右侧语法卡片已更新</div>
      </div>
    </div>

    <form class="composer" @submit="onSubmit">
      <input
        :value="draft"
        :disabled="sending"
        placeholder="输入你的下一句英文…"
        @input="emit('update:draft', ($event.target as HTMLInputElement).value)"
      />
      <button type="submit" class="btn primary" :disabled="sending || !draft.trim()">
        {{ sending ? '发送中…' : '发送' }}
      </button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { highlightBySpans } from '../utils/highlight'
import type { ChatMessage } from '../types'

const props = defineProps<{
  roleName: string
  turn: number
  messages: ChatMessage[]
  draft: string
  sending: boolean
}>()

const emit = defineEmits<{
  'update:draft': [value: string]
  send: []
}>()

const messagesEl = ref<HTMLElement | null>(null)

watch(
  () => props.messages.length,
  async () => {
    await nextTick()
    const el = messagesEl.value
    if (el) el.scrollTop = el.scrollHeight
  },
)

function onSubmit(e: Event) {
  e.preventDefault()
  emit('send')
}
</script>
