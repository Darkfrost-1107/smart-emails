import React from 'react'
import Header from './components/header'

export default function Layout({children} : React.PropsWithChildren) {
  return (
    <div className="flex flex-col h-full">
      <Header />
      <main className="p-4 flex-grow">
        {children}
      </main>
    </div>
  )
}
