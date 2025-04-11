import React from "react"
import ImportExcel from "../components/composables/importExcel"
import { EmailWithRecipient } from "../components/composables/dataDisplay/columns"

export function useImportExcel(action:(values : EmailWithRecipient[]) => void){
  
  const [open, setOpen] = React.useState(false)

  function Component() {
    return ImportExcel({
      open,
      onOpenChange: (open: boolean) => {
        console.log('Dialog open changed:', open)
        toogle()
      },
      handleSubmit(values) {
        action(values)
        toogle()
      },
    })
  }

  function toogle(){
    setOpen(!open)
  }
  
  return {
    Component,
    toogle,
  }
}