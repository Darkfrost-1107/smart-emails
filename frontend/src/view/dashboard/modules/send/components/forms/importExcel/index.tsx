import { Form } from '@/components/ui/form'
import React from 'react'
import { Button } from '@/components/ui/button'
import { useComponentForm } from './inputs'
import { useExportExcel } from '@/services/templates/imports/excel'
import { EmailWithRecipient } from '../../composables/dataDisplay/columns'

interface ImportExcelFormProps {
  onHandleSubmit: (el: EmailWithRecipient[]) => void;
}

export default function ImportExcelForm({onHandleSubmit}: ImportExcelFormProps) {
   // 1. Define your form.
  const {handleFileUpload, data} = useExportExcel()

  const {form, onSubmit,
    components: {
      NameColumnField,
      EmailColumnField,
      TemplateColumnField,
      FileField,
    }
  } = useComponentForm(async ({file, nameColumn, emailColumn, templateColumn}) => {
    console.log("accepted file", file)
    await handleFileUpload(file?.[0])

    console.log("imported data", data)
    const exportData = data.current.map((row) => ({
      recipent_name: row[nameColumn]?.toString() || "",
      recipent_email: row[emailColumn]?.toString() || "",
      name: row[templateColumn]?.toString() || "",
    }))
  
    onHandleSubmit(exportData)

  }) 
 
  // 2. Define a submit handler.  

  return (
    <Form {...form}>
      <form onSubmit={onSubmit} className="space-y-4">
        <FileField />
        <NameColumnField />
        <EmailColumnField />
        <TemplateColumnField />
        <Button type="submit">Importar</Button>
      </form>
    </Form>   
  )
}
