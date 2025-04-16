import logging
from typing import List, Dict, Any, Optional

from app.config import get_settings
from app.schemas.email import EmailRequest, EmailResponse
from app.core.providers import get_email_provider

settings = get_settings()
logger = logging.getLogger(__name__)

class EmailService:
    """
    Servicio para el envío de correos electrónicos.
    Actúa como una fachada para los diferentes proveedores de correo.
    """
    
    def __init__(self):
        # Obtener el proveedor de correo configurado
        self.provider = get_email_provider()
        logger.info(f"Servicio de correo inicializado con proveedor: {settings.EMAIL_PROVIDER}")
    
    async def send_email(self, email_data: EmailRequest) -> EmailResponse:
        """
        Envía un correo electrónico utilizando el proveedor configurado
        
        Args:
            email_data: Datos del correo a enviar
            
        Returns:
            EmailResponse: Resultado del envío
        """
        try:
            logger.info(f"Preparando correo con asunto: {email_data.subject}")
            
            # Delegar el envío al proveedor específico
            result = await self.provider.send_email(email_data)
            
            if result.success:
                logger.info(f"Correo enviado exitosamente mediante proveedor: {settings.EMAIL_PROVIDER}")
            else:
                logger.error(f"Error al enviar correo: {result.message}")
            
            return result
        
        except Exception as e:
            logger.exception(f"Error inesperado al enviar correo: {str(e)}")
            return EmailResponse(
                success=False,
                message=f"Error inesperado al enviar correo: {str(e)}"
            )