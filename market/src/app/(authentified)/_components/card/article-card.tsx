import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'

interface ArticleCardProps {
  title: string
  description: string
  price: number
}

const ArticleCard: React.FC<ArticleCardProps> = ({ title, description, price }) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardFooter>
        <p>{price}</p>
      </CardFooter>
    </Card>
  )
}

export default ArticleCard
