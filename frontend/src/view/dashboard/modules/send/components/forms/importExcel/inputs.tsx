"use client"

import { ComboBox } from "@/components/ui/combobox";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCallback } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

const formSchema = z.object({
  nameColumn: z.string().min(1, {
    message: "Introduzca una columna valida",
  }),
  emailColumn: z.string().min(1, {
    message: "Introduzca una columna valida",
  }),
  templateColumn: z.string().min(1, {
    message: "Introduzca una columna valida",
  }),
  file: typeof window === 'undefined' ? z.any() : z.instanceof(FileList).refine((file) => file?.length == 1, {
    message: "Por favor sube un archivo",
  })
})

export function useComponentForm(
  action: (values: z.infer<typeof formSchema>) => void
){

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      nameColumn: "",
      emailColumn: "",
      templateColumn: "",
      file: undefined,
    }
  })

  const fileRef = form.register("file")

  const onSubmit = 
    form.handleSubmit((values) => {
      console.log(values)    
      action(values)
    })

  type FileFieldProps = {
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void,
  }

  const FileField = useCallback(({onChange}: FileFieldProps) => {
    return (
      <FormField 
        control={form.control}
        name="file"
        render={() => 
          <FormItem>
            <FormLabel> Archivo Excel :</FormLabel>
            <FormMessage />
            <FormControl>
              <Input type="file" {...fileRef} onChange={(event) => {
                fileRef.onChange(event).then(() => onChange(event))
              }}/>
            </FormControl>
          </FormItem>
        }
      />
    )
  }, [form, fileRef])

  type ColumnInputType = {
    columns: string[],
  }

  const NameColumnField = useCallback(({columns}: ColumnInputType) => {
    return (
      <FormField
        control={form.control}
        name="nameColumn" 
        render={({field}) => 
          <FormItem>
            <FormLabel> Columna de Empresas :</FormLabel>
            <FormMessage />
            <FormControl>
              <ComboBox {...field} dataList={columns.map((element) => ({
                  label: element,
                  value: element,
                })
              )}/>
            </FormControl>
          </FormItem>
        }
      />
    )
  },[form])

  const EmailColumnField = useCallback(({columns}: ColumnInputType) => {
    return (
      <FormField
        control={form.control}
        name="emailColumn" 
        render={({field}) => 
          <FormItem>
            <FormLabel> Columna de Emails :</FormLabel>
            <FormMessage />
            <FormControl>
              <ComboBox {...field} dataList={columns.map((element) => ({
                  label: element,
                  value: element,
                })
              )}/>
            </FormControl>
          </FormItem>
        }
      />
    )
  },[form])

  const TemplateColumnField = useCallback(({columns}: ColumnInputType) => {
    return (
      <FormField
        control={form.control}
        name="templateColumn" 
        render={({field}) => 
          <FormItem>
            <FormLabel> Columna de Plantillas :</FormLabel>
            <FormMessage />
            <FormControl>
            <ComboBox {...field} dataList={columns.map((element) => ({
                  label: element,
                  value: element,
                })
              )}/>
            </FormControl>
          </FormItem>
        }
      />
    )
  },[form])

  return {
    formSchema,
    form,
    onSubmit,
    components: {
      NameColumnField,
      FileField,
      EmailColumnField,
      TemplateColumnField,
    }
  }
}