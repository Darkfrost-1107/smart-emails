import base64
import logging
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.utils import formataddr
from typing import List, Dict, Any, Optional

from app.config import get_settings
from app.core.providers.base import BaseEmailProvider
from app.core.providers.titan.auth import TitanAuth
from app.schemas.email import EmailRequest, EmailResponse, Attachment

settings = get_settings()
logger = logging.getLogger(__name__)

class TitanEmailProvider(BaseEmailProvider):
    """Implementación del proveedor de correo utilizando Titan Email"""
    
    def __init__(self):
        self.auth = TitanAuth()
        self.sender_email = settings.TITAN_SENDER_EMAIL
        self.sender_name = settings.APP_NAME
    
    async def send_email(self, email_data: EmailRequest) -> EmailResponse:
        """
        Envía un correo electrónico usando Titan Email SMTP
        
        Args:
            email_data: Datos del correo a enviar
            
        Returns:
            EmailResponse: Resultado del envío
        """
        try:
            # Crear el mensaje MIME
            msg = self._create_mime_message(email_data)
            
            # Obtener la conexión SMTP
            smtp_conn = self.auth.get_smtp_connection()
            
            try:
                # Enviar el correo
                logger.info(f"Enviando correo con asunto: {email_data.subject}")
                
                # Lista de destinatarios para el envío SMTP
                recipient_emails = [r.email for r in email_data.to_recipients]
                
                if email_data.cc_recipients:
                    recipient_emails.extend([r.email for r in email_data.cc_recipients])
                
                if email_data.bcc_recipients:
                    recipient_emails.extend([r.email for r in email_data.bcc_recipients])
                
                # Enviar el mensaje
                smtp_conn.send_message(msg)
                
                logger.info("Correo enviado exitosamente")
                
                return EmailResponse(
                    success=True,
                    message="Correo enviado exitosamente",
                    email_id=None
                )
            
            finally:
                # Cerrar la conexión SMTP
                smtp_conn.quit()
        
        except Exception as e:
            logger.exception(f"Error al enviar correo: {str(e)}")
            return EmailResponse(
                success=False,
                message=f"Error al enviar correo: {str(e)}"
            )
    
    def _create_mime_message(self, email_data: EmailRequest) -> MIMEMultipart:
        """
        Crea un mensaje MIME a partir de los datos del correo
        
        Args:
            email_data: Datos del correo
            
        Returns:
            MIMEMultipart: Mensaje MIME completo
        """
        # Crear el mensaje MIME
        msg = MIMEMultipart('mixed')
        
        # Configurar los encabezados
        msg['Subject'] = email_data.subject
        
        # Formatear correctamente la dirección del remitente
        from_addr = formataddr((self.sender_name, self.sender_email)) if self.sender_name else self.sender_email
        msg['From'] = from_addr
        
        # Configurar destinatarios
        to_addresses = []
        for recipient in email_data.to_recipients:
            to_addresses.append(formataddr((recipient.name, recipient.email)) if recipient.name else recipient.email)
        
        msg['To'] = ", ".join(to_addresses)
        
        # Configurar CC
        if email_data.cc_recipients:
            cc_addresses = []
            for recipient in email_data.cc_recipients:
                cc_addresses.append(formataddr((recipient.name, recipient.email)) if recipient.name else recipient.email)
            
            msg['Cc'] = ", ".join(cc_addresses)
        
        # Configurar importancia/prioridad
        if email_data.importance == "high":
            msg['Importance'] = 'high'
            msg['X-Priority'] = '1'
        elif email_data.importance == "low":
            msg['Importance'] = 'low'
            msg['X-Priority'] = '5'
        
        # Procesar el contenido (HTML o texto)
        if email_data.body_type.upper() == "HTML":
            # Si hay variables de plantilla, aplicarlas
            content = email_data.body
            if email_data.template_variables:
                for key, value in email_data.template_variables.items():
                    content = content.replace(f"{{{key}}}", str(value))
            
            # Crear parte HTML
            html_part = MIMEText(content, 'html', 'utf-8')
            
            # Crear también una parte de texto plano como alternativa
            # Versión simple: eliminar etiquetas HTML y mantener el texto
            import re
            text_content = re.sub('<[^<]+?>', '', content)
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            
            # Crear una parte alternativa para contenido de texto/html
            alternative = MIMEMultipart('alternative')
            alternative.attach(text_part)
            alternative.attach(html_part)
            
            msg.attach(alternative)
        else:
            # Texto plano
            content = email_data.body
            if email_data.template_variables:
                for key, value in email_data.template_variables.items():
                    content = content.replace(f"{{{key}}}", str(value))
            
            text_part = MIMEText(content, 'plain', 'utf-8')
            msg.attach(text_part)
        
        # Procesar adjuntos
        if email_data.attachments:
            for attachment_part in self.process_attachments(email_data.attachments):
                msg.attach(attachment_part)
        
        return msg
    
    def process_attachments(self, attachments: List[Attachment]) -> List[Any]:
        """
        Procesa los archivos adjuntos para el mensaje MIME
        
        Args:
            attachments: Lista de archivos adjuntos
            
        Returns:
            List[Any]: Lista de partes MIME para los adjuntos
        """
        attachment_parts = []
        
        for attachment in attachments:
            # Decodificar el contenido base64
            content = base64.b64decode(attachment.content)
            
            # Determinar el tipo MIME
            content_type = attachment.content_type
            if not content_type:
                content_type = mimetypes.guess_type(attachment.filename)[0] or 'application/octet-stream'
            
            # Crear la parte MIME según el tipo de contenido
            if content_type.startswith('image/'):
                part = MIMEImage(content, maintype='image', subtype=content_type.split('/')[1])
            else:
                part = MIMEApplication(content)
            
            # Configurar encabezados para el adjunto
            part.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            
            attachment_parts.append(part)
        
        return attachment_parts