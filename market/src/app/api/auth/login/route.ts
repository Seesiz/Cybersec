import { NextResponse } from 'next/server'

// Rate limit en mémoire (pour démo uniquement)
const RATE_LIMIT_WINDOW_MS = 60_000 // 60 secondes
const RATE_LIMIT_MAX = 3 // max 3 tentatives par fenêtre
const rateLimiter = new Map<string, number[]>() // ip -> timestamps (ms)

const USERS: Array<{ username: string; password: string; role?: string }> = [
  { username: 'alice', password: 'abcd' },
  { username: 'bob', password: 'bob123' },
  { username: 'eve', password: 'eve123' },
  { username: 'nyarodina', password: 'nyarodina123' },
  { username: 'randy', password: 'randy123' },
]

export async function POST(req: Request) {
  try {
    // Récupération IP (dev/proxy)
    const xff = req.headers.get('x-forwarded-for') || ''
    const ip = (xff.split(',')[0] || req.headers.get('x-real-ip') || 'unknown').trim()

    // Vérification du rate limit
    const now = Date.now()
    const recent = (rateLimiter.get(ip) ?? []).filter((ts) => now - ts < RATE_LIMIT_WINDOW_MS)
    if (recent.length >= RATE_LIMIT_MAX) {
      return NextResponse.json(
        { error: 'Trop de tentatives. Réessayez plus tard.' },
        { status: 429, headers: { 'Retry-After': '60' } }
      )
    }
    recent.push(now)
    rateLimiter.set(ip, recent)

    const { username, password } = (await req.json().catch(() => ({}))) as {
      username?: string
      password?: string
    }

    if (!username || !password)
      return NextResponse.json({ error: 'username et password sont requis' }, { status: 400 })

    const user = USERS.find((u) => u.username === username && u.password === password)
    if (!user) return NextResponse.json({ error: 'Identifiants invalides' }, { status: 401 })

    return NextResponse.json(
      { username: user.username, role: user.role ?? 'user' },
      { status: 200 }
    )
  } catch (err) {
    console.error('POST /api/auth/login error:', err)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}
