import { Card, CardContent } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import React from 'react'
import ImportExcelForm from '../../forms/importExcel';
import { EmailWithRecipient } from '../dataDisplay/columns';

interface ImportExcelProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;  
  handleSubmit: (ae: EmailWithRecipient[]) => void
}

export default function ImportExcel({handleSubmit, ...props}: ImportExcelProps) {

  return (
    <Dialog {...props} >
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Importar Remitentes desde Excel</DialogTitle>
          {/* <DialogDescription>
          </DialogDescription> */}
        </DialogHeader>
        <Card>
          <CardContent>
            <ImportExcelForm onHandleSubmit={handleSubmit}/>
          </CardContent>
        </Card>
      </DialogContent>
    </Dialog>
  )
}
