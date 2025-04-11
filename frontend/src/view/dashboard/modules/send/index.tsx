import React from 'react'
import Layout from '../..'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import DataDiplay from './components/composables/dataDisplay'

export default function SendEmail() {
  return (
    <Layout>
      <Card className="h-full">
        <CardHeader>
          Envia un email a tus clientes :3
        </CardHeader>
        <CardContent className="h-full">
        <Card className="h-full">
          <CardContent className="h-full">
            <DataDiplay />
          </CardContent>
          </Card>
        </CardContent>
      </Card>
    </Layout>
  )
}
