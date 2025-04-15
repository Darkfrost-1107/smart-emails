import { EmailWithRecipient } from "../components/composables/dataDisplay/columns";
import axios from "axios";
export async function sendEmails(emails: EmailWithRecipient[]) {
  try{
    for(const email of emails){
      if(email.recipent_email === "" || email.name === "" || email.recipent_name === ""){
        continue;
      }
      const {} = await axios.post("http://localhost:9800/api/emails/send-template",      )
    }
  } catch (error){
    console.log(error)
  }

}