import type { ErrorSpan } from '../types'

export function highlightBySpans(text: string, spans: ErrorSpan[] = [], className = 'err'): string {
  if (!spans.length) return escapeHtml(text)
  const sorted = [...spans].sort((a, b) => a.start - b.start)
  let html = ''
  let cursor = 0
  for (const span of sorted) {
    const start = Math.max(0, Math.min(span.start, text.length))
    const end = Math.max(start, Math.min(span.end, text.length))
    html += escapeHtml(text.slice(cursor, start))
    html += `<span class="${className}"${span.label ? ` data-tag="${escapeAttr(span.label)}"` : ''}>${escapeHtml(text.slice(start, end))}</span>`
    cursor = end
  }
  html += escapeHtml(text.slice(cursor))
  return html
}

function escapeHtml(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
}

function escapeAttr(value: string) {
  return escapeHtml(value).replaceAll("'", '&#39;')
}
