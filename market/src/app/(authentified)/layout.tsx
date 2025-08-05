import Header from './_components/header/header'

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="h-screen w-screen overflow-y-auto">
      <div className="relative flex min-h-screen flex-col">
        <Header />
        <main className="mx-auto w-full max-w-[1200px] p-5">{children}</main>
      </div>
    </div>
  )
}

export default Layout
