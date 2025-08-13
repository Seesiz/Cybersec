import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'

interface ArticleCardProps {
  label: string
  description: string
  price: number
}

const ArticleCard: React.FC<ArticleCardProps> = ({ label, description, price }) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>{label}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardFooter>
        <p>{price}</p>
      </CardFooter>
    </Card>
  )
}

export default ArticleCard
