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

export type EmailWithRecipient = EmailType & Recipient & {
  status?: "success" | "error" | "pending"
}

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
  },
  {
    accessorKey: "status",
    header: "Estado",
    cell: ({row}) => {
      return (
        <div className="flex items-center space-x-2">
          { row.getValue("status") === "success" ? 
            <span className="text-green-500">Enviado</span> :
            row.getValue("status") === "error" ?
            <span className="text-red-500">Error</span> :
            // row.getValue("status") === "pending" ?
            // <span className="text-yellow-500">Pendiente</span> :
            <span className="text-gray-500">Sin Enviar</span>
          }
        </div>
      )
    }
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
    setData,
  }
}