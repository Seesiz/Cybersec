import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(req: Request) {
  try {
    const body = (await req.json().catch(() => null)) as {
      content?: string
      id_article?: number
      user_name?: string
    } | null

    if (!body?.content || !body?.id_article || !body?.user_name) {
      return NextResponse.json(
        { error: 'content, id_article et user_name sont requis' },
        { status: 400 }
      )
    }

    const created = await prisma.comment.create({
      data: {
        content: body.content,
        id_article: body.id_article,
        user_name: body.user_name,
      },
    })

    return NextResponse.json(created, { status: 201 })
  } catch (err) {
    console.error('POST /api/comment error:', err)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}
