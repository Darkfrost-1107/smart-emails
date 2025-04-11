import {ColumnDef} from '@tanstack/react-table'
import React, { useEffect } from 'react'

type EmailType = {
  name: string,
  path?: string,
  size?: number,
  last_modified?: string,
}

type Recipient = {
  recipent_name: string,
  recipent_email: string
}

export type EmailWithRecipient = EmailType & Recipient

export const columns : ColumnDef<EmailWithRecipient>[] = [
  {
    accessorKey: "recipent_name",
    header: "Empresa",
  },
  {
    accessorKey: "recipent_email",
    header: "Email",
  },
  {
    accessorKey: "name",
    header: "Plantilla",
  }
]

export function useColumns() {

  const [data, setData] = React.useState<EmailWithRecipient[]>([])
  
  function importData(newData : EmailWithRecipient[]){
    console.log(newData)
    setData([...data, ...newData])
  }

  useEffect(() => {
    console.log("data,", data)
  }, [data])

  return {
    data, 
    importData,
  }
}