// // export async function Templates_importFromExcel(data: any){

// // }


// import { zodResolver } from "@hookform/resolvers/zod"
// import { useForm } from "react-hook-form"
// import { z } from "zod"
 
// const formSchema = z.object({
//   username: z.string().min(2, {
//     message: "Username must be at least 2 characters.",
//   }),
// })
 
// export function ProfileForm() {
//   // 1. Define your form.
//   const form = useForm<z.infer<typeof formSchema>>({
//     resolver: zodResolver(formSchema),
//     defaultValues: {
//       username: "",
//     },
//   })
 
//   // 2. Define a submit handler.
//   function onSubmit(values: z.infer<typeof formSchema>) {
//     // Do something with the form values.
//     // ✅ This will be type-safe and validated.
//     console.log(values)
//   }
// }

import { useRef, useState } from 'react';
import ExcelJS, { CellValue } from 'exceljs';

type RowData = {
  [key: string]: CellValue;
}

export function useExportExcel() {
  const data = useRef<RowData[]>([]);
  const columns = useRef<string[]>([]);
  const loading= useRef(false);
  const [fileName, setFileName] = useState('');

  const handleFileUpload = async (file: File) => {
    if (!file) return;

    loading.current = true
    setFileName(file.name);
    
    try {
      // Leer el archivo como ArrayBuffer
      const buffer = await file.arrayBuffer();
      
      // Crear un nuevo libro de trabajo
      const workbook = new ExcelJS.Workbook();
      
      // Cargar el archivo desde el buffer
      await workbook.xlsx.load(buffer);
      
      // Obtener la primera hoja del libro
      const worksheet = workbook.worksheets[0];
      
      // Extraer las columnas (encabezados)
      const cols: string[] = [];
      worksheet.getRow(1).eachCell((cell) => {
        cols.push(cell.value?.toString() ?? '');
      });
      columns.current = cols
      
      // Extraer los datos
      const rows : RowData[] = [];
      worksheet.eachRow((row, rowNumber) => {
        // Saltamos la primera fila (encabezados)
        if (rowNumber > 1) {
          const rowData: RowData = {};
          row.eachCell((cell, colNumber) => {
            rowData[cols[colNumber - 1]] = cell.value;
          });
          rows.push(rowData);
        }
      });
      
      data.current = rows
    } catch (error) {
      console.error('Error al procesar el archivo Excel:', error);
      alert('Error al procesar el archivo Excel');
    } finally {
      loading.current = false
    }
  };

  return {
    data: data,
    columns: columns,
    loading: loading,
    fileName,
    handleFileUpload,
  } 
}