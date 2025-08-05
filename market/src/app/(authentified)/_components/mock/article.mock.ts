interface IArticle {
  id: string
  title: string
  description: string
  price: number
  commentaire: { username: string; message: string }[]
}

export const articles: IArticle[] = [
  {
    id: '1',
    title: 'Article 1',
    description: 'Description 1',
    price: 100,
    commentaire: [
      { username: 'user1', message: 'commentaire 1' },
      { username: 'user2', message: 'commentaire 2' },
    ],
  },
  {
    id: '2',
    title: 'Article 2',
    description: 'Description 2',
    price: 200,
    commentaire: [
      { username: 'user1', message: 'commentaire 1' },
      { username: 'user2', message: 'commentaire 2' },
    ],
  },
  {
    id: '3',
    title: 'Article 3',
    description: 'Description 3',
    price: 300,
    commentaire: [
      { username: 'user1', message: 'commentaire 1' },
      { username: 'user2', message: 'commentaire 2' },
    ],
  },
  {
    id: '4',
    title: 'Article 4',
    description: 'Description 4',
    price: 400,
    commentaire: [
      { username: 'user1', message: 'commentaire 1' },
      { username: 'user2', message: 'commentaire 2' },
    ],
  },
  {
    id: '5',
    title: 'Article 5',
    description: 'Description 5',
    price: 500,
    commentaire: [
      { username: 'user1', message: 'commentaire 1' },
      { username: 'user2', message: 'commentaire 2' },
    ],
  },
]
