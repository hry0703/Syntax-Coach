import { api } from './client'
import type {
  ChatMessageResponse,
  CreateSessionResponse,
  GrammarCard,
  GrammarPoint,
  Mistake,
  Scene,
  UserProfile,
} from '../types'

export const MOCK_GRAMMAR_CARD: GrammarCard = {
  grammar_point_id: 'past_vs_present_perfect',
  title_zh: '现在完成时 vs 一般过去时',
  cefr: 'A2',
  original: 'I have went here yesterday, so medium is fine.',
  corrected: 'I went here yesterday, so medium is fine.',
  error_spans: [{ start: 2, end: 11, label: 'have + V-ed / 过去式冲突' }],
  rule_zh:
    'yesterday 是明确的过去时间点，应使用一般过去时（went）。have + 过去分词 表示与现在有关的完成，不能和 yesterday 这类具体过去时间连用；另外 go 的过去分词是 gone，不是 went。',
  examples: ['I went to this café yesterday.', 'I have been here before.'],
  severity: 'error',
}

export function fetchScenes() {
  return api.get<Scene[]>('/api/scenes')
}

export function createSession(sceneId: string, level?: string) {
  return api.post<CreateSessionResponse>('/api/chat/sessions', {
    scene_id: sceneId,
    level,
  })
}

export function sendMessage(sessionId: string, content: string) {
  return api.post<ChatMessageResponse>(`/api/chat/sessions/${sessionId}/messages`, {
    content,
  })
}

export function fetchGrammarPoints() {
  return api.get<GrammarPoint[]>('/api/grammar-points')
}

export function fetchMistakes() {
  return api.get<Mistake[]>('/api/mistakes')
}

export function createMistake(payload: {
  grammar_point_id: string
  original: string
  corrected: string
  scene_id?: string
  rule_zh?: string
}) {
  return api.post<Mistake>('/api/mistakes', payload)
}

export function fetchProfile() {
  return api.get<UserProfile>('/api/profile')
}

export function updateProfile(profile: UserProfile) {
  return api.patch<UserProfile>('/api/profile', profile)
}
