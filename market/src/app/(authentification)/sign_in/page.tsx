'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useSession } from '@/provider/session'

const Page = () => {
  const [username, setUsername] = useState('')
  const { login } = useSession()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (username.trim()) {
      login(username)
    }
  }

  return (
    <div className="flex items-center justify-center h-screen w-screen">
      <Card className="max-w-[400px] w-full">
        <CardHeader>
          <CardTitle>Connexion</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-4">
              <Input
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
              />

              <Button type="submit">Se connecter</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default Page
