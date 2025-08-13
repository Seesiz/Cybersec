import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(req: Request) {
  try {
    const url = new URL(req.url)
    const q = url.searchParams.get('q') ?? ''

    // Exemple d'attaque: q = ' OR '1'='1
    const sql = `SELECT id, content, id_article, user_name FROM "comment" WHERE user_name = '${q}'`

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rows = await prisma.$queryRawUnsafe<any[]>(sql)
    return NextResponse.json({ vulnerable: true, sql, rows })
  } catch (err) {
    console.error('GET /api/comment/search (vulnérable) error:', err)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}
