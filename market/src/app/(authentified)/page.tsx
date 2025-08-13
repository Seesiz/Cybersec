'use client'

import Link from 'next/link'
import ArticleCard from './_components/card/article-card'
import { useEffect, useState } from 'react'

export interface IArticle {
  id: string
  label: string
  comment?: {
    id: number
    content: string
    id_article: number
    user_name: string
    article: IArticle
  }[]
}

const Page = () => {
  const [articles, setArticles] = useState<IArticle[]>([])

  useEffect(() => {
    fetch('http://localhost:3000/api/article', {
      cache: 'no-store',
    })
      .then((res) => res.json())
      .then((data) => setArticles(data))
  }, [])

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {articles.map((article) => (
        <Link href={`/article/${article.id}`} key={article.id}>
          <ArticleCard {...article} description="Description article" price={200} />
        </Link>
      ))}
    </div>
  )
}

export default Page
