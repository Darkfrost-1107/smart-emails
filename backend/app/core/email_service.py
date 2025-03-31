import logging
import mimetypes
import base64
from typing import List, Dict, Any, Optional
import httpx

from app.config import get_settings
from app.core.auth import MSGraphAuth
from app.schemas.email import EmailRequest, EmailResponse, EmailRecipient, Attachment

settings = get_settings()
logger = logging.getLogger(__name__)

class EmailService:
    """Servicio para el envío de correos electrónicos"""
    
    def __init__(self):
        self.auth = MSGraphAuth()
        self.ms_graph_endpoint = settings.MS_GRAPH_ENDPOINT
    
    async def send_email(self, email_data: EmailRequest) -> EmailResponse:
        
        try:
            # Obtener encabezados 
            headers = self.auth.get_auth_headers()
            
            # Crear el cuerpo del mensaje
            message = self._create_message_body(email_data)
            
            # Preparar la carga para la API
            payload = {
                "message": message,
                "saveToSentItems": email_data.save_to_sent_items
            }
            
            logger.info(f"Enviando correo con asunto: {email_data.subject}")
            
            # Configurar cliente HTTP con timeout
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f'{self.ms_graph_endpoint}/me/sendMail',
                    headers=headers,
                    json=payload
                )
                
                # Verificar respuesta
                if response.status_code == 202:
                    logger.info("Correo enviado exitosamente")
                    return EmailResponse(
                        success=True,
                        message="Correo enviado exitosamente",
                        email_id=None  # Graph API no devuelve ID de correo en esta operación
                    )
                else:
                    error_msg = f"Error al enviar correo: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return EmailResponse(
                        success=False,
                        message=error_msg
                    )
                
        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error al enviar correo: {str(e)}")
            return EmailResponse(
                success=False,
                message=f"HTTP error al enviar correo: {str(e)}"
            )
        except Exception as e:
            logger.exception(f"Error al enviar correo: {str(e)}")
            return EmailResponse(
                success=False,
                message=f"Error al enviar correo: {str(e)}"
            )
    
    def _process_attachment(self, file_data: Attachment) -> dict:
        """Procesa un archivo adjunto desde la solicitud"""
        return {
            '@odata.type': '#microsoft.graph.fileAttachment',
            'name': file_data.filename,
            'contentType': file_data.content_type or mimetypes.guess_type(file_data.filename)[0] or 'application/octet-stream',
            'contentBytes': file_data.content
        }
    
    def _create_message_body(self, email_data: EmailRequest) -> dict:
        """Crea el cuerpo del mensaje para la API de Microsoft Graph"""
        # Procesar destinatarios
        to_recipients = [{"emailAddress": {"address": r.email, "name": r.name}} for r in email_data.to_recipients]
        
        cc_recipients = []
        if email_data.cc_recipients:
            cc_recipients = [{"emailAddress": {"address": r.email, "name": r.name}} for r in email_data.cc_recipients]
        
        bcc_recipients = []
        if email_data.bcc_recipients:
            bcc_recipients = [{"emailAddress": {"address": r.email, "name": r.name}} for r in email_data.bcc_recipients]
        
        # Procesar adjuntos
        attachments = []
        if email_data.attachments:
            attachments = [self._process_attachment(attachment) for attachment in email_data.attachments]
        
        # Aplicar variables de plantilla si están disponibles
        content = email_data.body
        if email_data.template_variables:
            for key, value in email_data.template_variables.items():
                content = content.replace(f"{{{key}}}", str(value))
        
        # Crear el mensaje
        message = {
            'subject': email_data.subject,
            'body': {
                'contentType': email_data.body_type,
                'content': content
            },
            'toRecipients': to_recipients,
            'importance': email_data.importance
        }
        print(  message)
        
        if cc_recipients:
            message['ccRecipients'] = cc_recipients
        
        if bcc_recipients:
            message['bccRecipients'] = bcc_recipients
        
        if attachments:
            message['attachments'] = attachments
        
        return message