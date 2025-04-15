import logging
import mimetypes
from typing import List, Dict, Any, Optional
import httpx

from app.config import get_settings
from app.core.providers.base import BaseEmailProvider
from app.core.providers.outlook.auth import OutlookAuth
from app.schemas.email import EmailRequest, EmailResponse, Attachment

settings = get_settings()
logger = logging.getLogger(__name__)

class OutlookEmailProvider(BaseEmailProvider):
    """Implementación del proveedor de correo utilizando Microsoft Graph API para Outlook"""
    
    def __init__(self):
        self.auth = OutlookAuth()
        self.ms_graph_endpoint = settings.MS_GRAPH_ENDPOINT
    
    async def send_email(self, email_data: EmailRequest) -> EmailResponse:
        """
        Envía un correo electrónico usando Microsoft Graph API
        
        Args:
            email_data: Datos del correo a enviar
            
        Returns:
            EmailResponse: Resultado del envío
        """
        try:
            # Obtener encabezados de autenticación
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
    
    def _create_message_body(self, email_data: EmailRequest) -> dict:
        """
        Crea el cuerpo del mensaje para la API de Microsoft Graph
        
        Args:
            email_data: Datos del correo
            
        Returns:
            dict: Diccionario con el cuerpo del mensaje en formato de Graph API
        """
        # Procesar destinatarios
        to_recipients = [{"emailAddress": {"address": r.email, "name": r.name}} for r in email_data.to_recipients]
        
        cc_recipients = []
        if email_data.cc_recipients:
            cc_recipients = [{"emailAddress": {"address": r.email, "name": r.name}} for r in email_data.cc_recipients]
        
        bcc_recipients = []
        if email_data.bcc_recipients:
            bcc_recipients = [{"emailAddress": {"address": r.email, "name": r.name}} for r in email_data.bcc_recipients]
        
        # Procesar adjuntos
        attachments = self.process_attachments(email_data.attachments) if email_data.attachments else []
        
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
        
        if cc_recipients:
            message['ccRecipients'] = cc_recipients
        
        if bcc_recipients:
            message['bccRecipients'] = bcc_recipients
        
        if attachments:
            message['attachments'] = attachments
        
        return message
    
    def process_attachments(self, attachments: List[Attachment]) -> List[Dict[str, Any]]:
        """
        Procesa los archivos adjuntos para Microsoft Graph API
        
        Args:
            attachments: Lista de archivos adjuntos
            
        Returns:
            List[Dict[str, Any]]: Lista de adjuntos en formato de Graph API
        """
        if not attachments:
            return []
        
        graph_attachments = []
        
        for attachment in attachments:
            mime_type = attachment.content_type or mimetypes.guess_type(attachment.filename)[0] or 'application/octet-stream'
            
            graph_attachments.append({
                '@odata.type': '#microsoft.graph.fileAttachment',
                'name': attachment.filename,
                'contentType': mime_type,
                'contentBytes': attachment.content
            })
        
        return graph_attachments