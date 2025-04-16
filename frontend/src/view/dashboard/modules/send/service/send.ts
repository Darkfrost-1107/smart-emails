import api from "@/services/templates/config";
import { EmailWithRecipient } from "../components/composables/dataDisplay/columns";

/**
 * Envia un email a los destinatarios
 */
export async function sendEmails(emails: EmailWithRecipient[]) {
  const newEmails : EmailWithRecipient[] = []
  try{
    for(const key in emails){
      // await setTimeout(() => {}, 1000)
      const email = emails[key]
      console.log(email)
      if(email.recipent_email === "" || email.name === "" || email.recipent_name === "" || email.status === "success"){
        continue;
      }
      const {} = await api.post("emails/send-template", {
        template_name: email.name,
        subject: "Bienvenido a Beryllium",
        to_recipients: email.recipent_email,
        // Verificar
        body_type: "HTML",
// # TODO Verificar o estimar el importance
        importance: "normal",
        template_variables: {
          EMPRESA: email.recipent_name,
        }
      })
      newEmails[key] = { ...emails[key], 
        status: "success" 
      } 
    }
    return newEmails
  } catch (error){
    console.log(error)
    return emails
  }

}