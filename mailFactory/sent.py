
import os 
from pathlib import Path
import httpx
from dotenv import load_dotenv
from ms_token import get_access_token , MS_GRAPH_ENDPOINT
from outock import create_attachment

def draft_message_body(subject: str, html_content: str, attachments: list):
    message = {
        'subject': subject,
        'body': {
            'contentType': 'HTML',
            'content': html_content.replace("[EMPRESA]", "<> Beryllium <>")
            },
        'toRecipients': [
            {
                'emailAddress': {
                    'address': 'gabrielalbertokb@outlook.com'
                }
            },
            # {
            #     'emailAddress': {
            #         'address': 'marrondaniel20@gmail.com'
            #     }
            # },
            # {
            #     'emailAddress': {
            #         'address': 'danielmarronc@gmail.com'
            #     }
            # },
            {
                'emailAddress': {
                    'address': 'gbernedok@unsa.edu.pe'
                }
            },
            #  {
            #     'emailAddress': {
            #         'address': 'hchalco@unsa.edu.pe'
            #     }
            # },
            # {
            #     'emailAddress': {
            #         'address': 'spacori@unsa.edu.pe'
            #     }
            # },
            # {
            #     'emailAddress': {
            #         'address': 'administracion@berylliumdev.com'
            #     }
            # }
        ],
        'ccRecipients': [
            {
                'emailAddress': {
                    'address': 'xxxxxxxxxxxx@gmail.com'
                }
            }
        ],
        'importance': 'normal',
        'attachments': attachments
    }

    return message

def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES  = ['Mail.ReadWrite','Mail.Send', 'User.Read']
    
    try:
        access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        dir_attachments = Path('./attachments')
        dir_attachments.mkdir(exist_ok=True) 
        attachments = []
        
        if dir_attachments.exists():
            attachments = [create_attachment(file) for file in dir_attachments.iterdir() if file.is_file()]
        
        empresa = "Mi Empresa S.A."  # Valor que reemplazará {empresa}

        # Leer el template HTML desde el archivo
        with open("test.html", "r", encoding="utf-8") as file:
        # with open("beryllium-email.html", "r", encoding="utf-8") as file:
            html_template = file.read()

        # Reemplazar la variable en el template
        html_content = html_template  

        endpoint = f'{MS_GRAPH_ENDPOINT}/me/sendMail'
        message = draft_message_body(
            subject='Bienvenida a Beryllium',
            html_content=html_content,
            attachments=attachments
        )
        payload = {
            "message": message,
            "saveToSentItems": True
        }

        # Enviar con timeout y manejo de errores
        with httpx.Client(timeout=30) as client:
            response = client.post(
                endpoint,
                headers=headers,
                json=payload
            )
            response.raise_for_status()  # Lanza excepción para códigos 4xx/5xx
            
            if response.status_code == 202:
                print("Correo enviado exitosamente!")
            else:
                print(f"Respuesta inesperada: {response.status_code} - {response.text}")


    except httpx.HTTPStatusError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error: {e}')
if __name__ == '__main__':
    main()