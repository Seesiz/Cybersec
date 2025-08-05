import Link from 'next/link'
import ArticleCard from './_components/card/article-card'
import { articles } from './_components/mock/article.mock'

const Page = () => {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {articles.map((article) => (
        <Link href={`/article/${article.id}`} key={article.id}>
          <ArticleCard {...article} />
        </Link>
      ))}
    </div>
  )
}

export default Page
