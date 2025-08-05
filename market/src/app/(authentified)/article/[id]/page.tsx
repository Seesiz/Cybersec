'use client'

import { useParams } from 'next/navigation'
import { useState } from 'react'
import { articles } from '../../_components/mock/article.mock'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useSession } from '@/provider/session'

const Page = () => {
  const { id } = useParams<{ id: string }>()
  const [comment, setComment] = useState('')
  const { user } = useSession()

  const articleIndex = articles.findIndex((article) => article.id === id)
  const article = articles[articleIndex]

  const handleAddComment = () => {
    if (!comment.trim() || !user) return

    articles[articleIndex].commentaire.push({
      username: user.username,
      message: comment,
    })

    setComment('')
  }

  if (!article) {
    return <div>Article non trouvé</div>
  }

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h1>{article.title}</h1>
        <p>{article.description}</p>
        <p>{article.price}</p>
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
            <Button onClick={handleAddComment}>Envoyer</Button>
          </div>
          {article.commentaire.map((commentaire, index) => (
            <div
              key={`${commentaire.username}-${index}`}
              className="flex w-fit flex-col gap-2 rounded-xl rounded-tl-none bg-gray-50 p-2 px-5"
            >
              <b>{commentaire.username}</b>
              <p dangerouslySetInnerHTML={{ __html: commentaire.message as string }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Page
