import { Form } from '@/components/ui/form'
import React, { useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useComponentForm } from './inputs'
import { useExportExcel } from '@/services/templates/imports/excel'
import { EmailWithRecipient } from '../../composables/dataDisplay/columns'

interface ImportExcelFormProps {
  onHandleSubmit: (el: EmailWithRecipient[]) => void;
}

export default function ImportExcelForm({onHandleSubmit}: ImportExcelFormProps) {
   // 1. Define your form.
  const {handleFileUpload, data, columns, fileName} = useExportExcel()

  const [cols, setCols] = React.useState<string[]>([])
  const [refresh, setRefresh] = React.useState(false)

  useEffect(() => {
    console.log("columns", columns.current)
    setCols(columns.current)
  }, [fileName, columns, refresh])

  const {form, onSubmit,
    components: {
      NameColumnField,
      EmailColumnField,
      TemplateColumnField,
      FileField,
    }
  } = useComponentForm(async ({nameColumn, emailColumn, templateColumn}) => {

    console.log("imported data", data)
    const exportData : EmailWithRecipient[] = data.current.map((row) => ({
      recipent_name: row[nameColumn]?.toString() || "",
      recipent_email: row[emailColumn]?.toString() || "",
      name: row[templateColumn]?.toString() || "",
      status: "pending",
    }))
  
    onHandleSubmit(exportData)
  }) 
 
  // 2. Define a submit handler.  

  return (
    <Form {...form}>
      <form onSubmit={onSubmit} className="space-y-4">
        <FileField onChange={async (event) => {
          if(event.target.files != null){
            await handleFileUpload(event.target.files[0])
            setRefresh(!refresh)
          }
        }}/>
        <NameColumnField columns={cols}/>
        <EmailColumnField columns={cols}/>
        <TemplateColumnField columns={cols}/>
        <Button type="submit">Importar</Button>
      </form>
    </Form>   
  )
}
