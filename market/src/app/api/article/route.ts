import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    const res = await prisma.article.findMany()
    return NextResponse.json(res)
  } catch (err) {
    console.error('GET /api/article error:', err)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}
