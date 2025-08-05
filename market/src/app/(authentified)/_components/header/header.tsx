'use client'

import { Button } from '@/components/ui/button'
import { useSession } from '@/provider/session'
import { LogOut } from 'lucide-react'

const Header = () => {
  const { user, logout } = useSession()
  return (
    <div className="bg-primary sticky top-0 z-50 flex h-[70px] items-center justify-between p-4 px-10">
      <h1 className="text-white">
        Welcome to the market <b>{user?.username}</b>
      </h1>
      <Button variant="secondary" onClick={logout}>
        <LogOut />
      </Button>
    </div>
  )
}

export default Header
