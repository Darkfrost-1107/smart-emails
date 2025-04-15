"use client"

import DataTable from '@/components/ui/data-table'
import React from 'react'
import { columns, useColumns } from './columns'
import { Text } from '@/components/ui/text'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { useImportExcel } from '../../../hooks/useImportExcel'
import { sendEmails } from '../../../service/send'

export default function DataDiplay() {
  
  const {data, importData} = useColumns()
  const {Component: ImportExcel, toogle} = useImportExcel(importData)

  return (
    <div className="flex flex-col gap-4 h-full">
      <Card>
        <CardContent className="flex flex-row items-center justify-between">
          <Text variant="h1" >
            Envia Emails
          </Text>
          <div className='flex gap-2 items-center'>
            <Button
              onClick={() => {
                sendEmails(data)
                console.log('Enviado Exitosamente') 
              }}
            >
              Enviar a Todos
            </Button>
            <Button
              onClick={() => {
                // handleFileUpload
                toogle()
                console.log('Importar remitentes')
              }}
            >
              Importar Remitentes
            </Button>
          </div>
        </CardContent>
      </Card>
      <DataTable columns={columns} data={data} className="flex-grow h-full" /> 
      <ImportExcel />
    </ div>
  )
}
