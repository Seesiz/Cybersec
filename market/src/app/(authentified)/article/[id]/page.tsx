'use client'

import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
// import { useSession } from '@/provider/session'
import { IArticle } from '../../page'
import { useSession } from '@/provider/session'

const Page = () => {
  const { id } = useParams<{ id: string }>()
  const [comment, setComment] = useState('')
  const { user } = useSession()

  const [article, setArticle] = useState<IArticle | null>(null)

  useEffect(() => {
    fetch(`http://localhost:3000/api/article/${id}`, {
      cache: 'no-store',
    })
      .then((res) => res.json())
      .then((data) => setArticle(data))
  }, [id])

  if (!article) {
    return <div>Article non trouvé</div>
  }

  const handleAddComment = async () => {
    if (!comment.trim()) return
    try {
      const res = await fetch('/api/comment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: comment,
          id_article: Number(id),
          user_name: user?.username,
        }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const created = await res.json()
      setArticle({ ...article, comment: [...(article.comment ?? []), created] })
      setComment('')
    } catch (e) {
      console.error(e)
    }
  }

  const handleSearchComment = async () => {
    if (!comment.trim()) return
    try {
      const res = await fetch(`/api/comment/search?q=${encodeURIComponent(comment)}`, {
        method: 'GET',
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      // data.rows contient le résultat de la requête vulnérable
      setArticle({ ...article, comment: data?.rows ?? [] })
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1>{article.label}</h1>
      </div>

      <p>Injection test</p>
      <p>
        {`<img src="x" onError="const adDiv = document.createElement('div'); adDiv.style = 'position: fixed; top: 10px; right: 10px; background-color: yellow; padding: 10px; border: 2px solid red; z-index: 9999;'; adDiv.innerHTML = '<h3>PUBLICITÉ</h3><p>Achetez notre nouveau produit !</p>'; document.body.appendChild(adDiv);" />`}
      </p>
      <div className="flex flex-col gap-4">
        <h2>Commentaires</h2>
        <div className="flex flex-col gap-4 rounded-2xl border p-4">
          <div className="flex gap-2">
            <Input
              placeholder="Commentaire"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />

            <div className="flex gap-2">
              <Button onClick={handleAddComment}>Envoyer</Button>
              <Button onClick={handleSearchComment}>Search</Button>
            </div>
          </div>
          {article?.comment?.map((commentaire, index) => (
            <div
              key={`${commentaire.user_name}-${index}`}
              className="flex w-fit flex-col gap-2 rounded-xl rounded-tl-none bg-gray-50 p-2 px-5"
            >
              <b>{commentaire.user_name}</b>
              <p dangerouslySetInnerHTML={{ __html: commentaire.content }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Page
