export type ErrorSpan = {
  start: number
  end: number
  label: string
}

export type GrammarCard = {
  grammar_point_id: string
  title_zh: string
  cefr: string
  original: string
  corrected: string
  error_spans: ErrorSpan[]
  rule_zh: string
  examples: string[]
  severity: 'error' | 'suggestion'
}

export type Scene = {
  id: string
  title_zh: string
  title_en: string
  role: string
  level: string
  description: string
}

export type GrammarPoint = {
  id: string
  title_zh: string
  cefr: string
  category: string
  rule_zh: string
  wrong_patterns: string[]
  examples: string[]
  contrast?: string | null
}

export type CreateSessionResponse = {
  session_id: string
  scene_id: string
  status: 'active'
}

export type ChatMessageResponse = {
  reply: string
  grammar_card: GrammarCard | null
  turn: number
}

export type Mistake = {
  id: string
  grammar_point_id: string
  original: string
  corrected: string
  scene_id?: string | null
  rule_zh?: string | null
  mastered: boolean
}

export type UserProfile = {
  level: 'A2' | 'B1' | 'B2'
  goal: 'speaking' | 'business' | 'exam'
  correction_strictness: 'light' | 'standard' | 'strict'
  explanation_detail: 'brief' | 'standard' | 'detailed'
  show_terms: boolean
}

export type ChatMessage = {
  id: string
  role: 'agent' | 'user'
  content: string
  who: string
  active?: boolean
  errorSpans?: ErrorSpan[]
}
