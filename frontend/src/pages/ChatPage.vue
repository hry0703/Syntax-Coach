<template>
  <div class="page-shell chat-shell" style="overflow-x: auto">
    <div class="frame">
      <TopBar
        :scene-label="sceneLabel"
        show-end-session
        @end-session="router.push('/')"
      />
      <div class="workspace">
        <ChatPane
          :role-name="scene?.role ?? 'Coach'"
          :turn="turn"
          :messages="messages"
          :draft="draft"
          :sending="sending"
          @update:draft="draft = $event"
          @send="handleSend"
        />
        <GrammarCardPanel :card="card" @add-weak-point="handleAddWeakPoint" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TopBar from '../components/TopBar.vue'
import ChatPane from '../components/ChatPane.vue'
import GrammarCardPanel from '../components/GrammarCard.vue'
import {
  MOCK_GRAMMAR_CARD,
  createMistake,
  createSession,
  fetchScenes,
  sendMessage,
} from '../api/endpoints'
import type { ChatMessage, GrammarCard, Scene } from '../types'

const route = useRoute()
const router = useRouter()
const sceneId = computed(() => String(route.params.sceneId || ''))

const scene = ref<Scene | null>(null)
const sessionId = ref<string | null>(null)
const messages = ref<ChatMessage[]>([])
const card = ref<GrammarCard | null>(MOCK_GRAMMAR_CARD)
const draft = ref('')
const turn = ref(1)
const sending = ref(false)

const sceneLabel = computed(() => {
  if (!scene.value) return '场景加载中…'
  return `场景：${scene.value.title_zh} · ${scene.value.level}`
})

onMounted(async () => {
  try {
    const scenes = await fetchScenes()
    const found = scenes.find((s) => s.id === sceneId.value) ?? null
    scene.value = found
    const opener =
      found?.id === 'coffee_shop'
        ? 'Hi! What can I get for you today?'
        : `Let's practice: ${found?.title_en ?? sceneId.value}. How would you start?`
    messages.value = [
      {
        id: 'agent-1',
        role: 'agent',
        who: found?.role ?? 'Coach',
        content: opener,
      },
    ]
    const session = await createSession(sceneId.value, found?.level)
    sessionId.value = session.session_id
  } catch {
    scene.value = {
      id: sceneId.value,
      title_zh: sceneId.value,
      title_en: sceneId.value,
      role: 'Coach',
      level: 'B1',
      description: '',
    }
    messages.value = [
      {
        id: 'agent-1',
        role: 'agent',
        who: 'Coach',
        content: 'Hi! What can I get for you today?',
      },
    ]
    card.value = MOCK_GRAMMAR_CARD
  }
})

async function handleSend() {
  const content = draft.value.trim()
  if (!content) return
  sending.value = true
  draft.value = ''

  const userId = `user-${Date.now()}`
  messages.value = [
    ...messages.value.map((m) => ({ ...m, active: false })),
    { id: userId, role: 'user', who: 'You', content, active: true },
  ]

  try {
    const sid = sessionId.value ?? 'local-stub'
    const res = await sendMessage(sid, content)
    turn.value = res.turn
    if (res.grammar_card) {
      card.value = res.grammar_card
      messages.value = messages.value.map((m) =>
        m.id === userId
          ? { ...m, errorSpans: res.grammar_card?.error_spans, active: true }
          : { ...m, active: false },
      )
    }
    messages.value = [
      ...messages.value,
      {
        id: `agent-${Date.now()}`,
        role: 'agent',
        who: scene.value?.role ?? 'Coach',
        content: res.reply,
      },
    ]
  } catch {
    card.value = { ...MOCK_GRAMMAR_CARD, original: content }
    messages.value = [
      ...messages.value,
      {
        id: `agent-${Date.now()}`,
        role: 'agent',
        who: scene.value?.role ?? 'Coach',
        content: 'Got it. (离线 stub：后端未连通时使用本地语法卡片样例。)',
      },
    ]
  } finally {
    sending.value = false
  }
}

async function handleAddWeakPoint() {
  if (!card.value) return
  try {
    await createMistake({
      grammar_point_id: card.value.grammar_point_id,
      original: card.value.original,
      corrected: card.value.corrected,
      scene_id: sceneId.value,
      rule_zh: card.value.rule_zh,
    })
    alert('已加入薄弱语法点（内存 stub，重启后端会清空）')
  } catch {
    alert('加入失败：请确认后端已启动')
  }
}
</script>
