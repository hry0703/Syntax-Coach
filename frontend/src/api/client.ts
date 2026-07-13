async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `Request failed: ${res.status}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: 'POST', body: body ? JSON.stringify(body) : undefined }),
  patch: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: 'PATCH', body: body ? JSON.stringify(body) : undefined }),
}
