'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { getSession, setSession } from '@/utils/session-storage'

type User = {
  username: string
} | null
type SessionContextType = {
  user: User
  login: (username: string, redirectPath?: string) => void
  logout: () => void
}

const SessionContext = createContext<SessionContextType>({
  user: null,
  login: () => {},
  logout: () => {},
})

export const useSession = () => useContext(SessionContext)

const publicPages = ['/sign_in']

const SessionProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    const username = getSession('username')
    if (username) {
      setUser({ username })
    } else if (!publicPages.includes(pathname)) {
      router.push('/sign_in')
    }
    setLoading(false)
  }, [router, pathname])

  const login = (username: string, redirectPath: string = '/') => {
    setSession('username', username)
    setUser({ username })
    router.push(redirectPath)
  }

  const logout = () => {
    setSession('username', '')
    setUser(null)
    router.push('/sign_in')
  }

  if (loading) {
    return <div className="flex items-center justify-center h-screen w-screen">Chargement...</div>
  }

  if (publicPages.includes(pathname)) {
    return (
      <SessionContext.Provider value={{ user, login, logout }}>{children}</SessionContext.Provider>
    )
  }

  return (
    <SessionContext.Provider value={{ user, login, logout }}>
      {user ? children : null}
    </SessionContext.Provider>
  )
}

export default SessionProvider
