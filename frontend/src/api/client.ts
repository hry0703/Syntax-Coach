/** 后端统一信封；成功 code === 0，业务在 data。 */
export type ApiEnvelope<T> = {
  code: number
  data: T | null
  errorMsg: string | null
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })

  const text = await res.text()
  let envelope: ApiEnvelope<T> | null = null
  try {
    envelope = text ? (JSON.parse(text) as ApiEnvelope<T>) : null
  } catch {
    throw new Error(text || `Request failed: ${res.status}`)
  }

  if (!envelope || typeof envelope.code !== 'number') {
    throw new Error(text || `Request failed: ${res.status}`)
  }

  // 业务成败只看 code（0 = 成功）
  if (envelope.code !== 0) {
    const msg = envelope.errorMsg || String(envelope.code)
    throw new Error(`[${envelope.code}] ${msg}`)
  }

  return envelope.data as T
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: 'POST', body: body ? JSON.stringify(body) : undefined }),
  patch: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: 'PATCH', body: body ? JSON.stringify(body) : undefined }),
}
