import json
import logging
import base64
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.schemas.email import EmailRequest, EmailResponse, EmailRecipient, Attachment
from app.core.email_service import EmailService
from app.core.template_service import TemplateService
from app.api.deps import get_email_service, get_template_service, get_auth_headers

router = APIRouter()
logger = logging.getLogger(__name__)

class TemplateEmailRequest(BaseModel):
    template_name: str
    subject: str
    to_recipients: str  # Lista de emails separados por coma
    cc_recipients: Optional[str] = None
    bcc_recipients: Optional[str] = None
    importance: str = "normal"
    template_variables: Optional[Dict[str, Any]] = None
    attachments: Optional[List[Attachment]] = None

@router.post("/send", response_model=EmailResponse)
async def send_email(
    email_data: EmailRequest,
    background_tasks: BackgroundTasks,
    email_service: EmailService = Depends(get_email_service),
    headers: dict = Depends(get_auth_headers)
):
    """
    Envía un correo electrónico con todos los parámetros especificados.
    
    - **subject**: Asunto del correo
    - **body**: Contenido del correo
    - **body_type**: Tipo de contenido ("HTML" o "Text")
    - **to_recipients**: Lista de destinatarios principales
    - **cc_recipients**: Lista de destinatarios en copia (opcional)
    - **bcc_recipients**: Lista de destinatarios en copia oculta (opcional)
    - **importance**: Importancia del correo ("low", "normal", "high")
    - **attachments**: Lista de archivos adjuntos (opcional)
    - **save_to_sent_items**: Guardar en elementos enviados (default: true)
    - **template_variables**: Variables para plantillas (opcional)
    """
    try:
        result = await email_service.send_email(email_data)
        if not result.success:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": result.message}
            )
        return result
    except Exception as e:
        logger.exception(f"Error al enviar correo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al enviar correo: {str(e)}")

@router.post("/send-template", response_model=EmailResponse)
async def send_template_email(
    email_request: TemplateEmailRequest,
    background_tasks: BackgroundTasks,
    email_service: EmailService = Depends(get_email_service),
    template_service: TemplateService = Depends(get_template_service),
    headers: dict = Depends(get_auth_headers)
):
    """
    Envía un correo utilizando una plantilla HTML con variables.
    
    - **template_name**: Nombre de la plantilla a utilizar
    - **subject**: Asunto del correo
    - **to_recipients**: Lista de destinatarios principales (separados por coma)
    - **cc_recipients**: Lista de destinatarios en copia (separados por coma, opcional)
    - **bcc_recipients**: Lista de destinatarios en copia oculta (separados por coma, opcional)
    - **importance**: Importancia del correo ("low", "normal", "high")
    - **template_variables**: Variables para la plantilla en formato JSON (opcional)
    - **attachments**: Lista de objetos Attachment con archivos codificados en Base64 (opcional)
    """
    try:
        # Verificar que la plantilla existe
        try:
            template_content = template_service.get_template_content(email_request.template_name)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Plantilla '{email_request.template_name}' no encontrada")
        
        # Convertir listas de destinatarios
        to_list = [EmailRecipient(email=email.strip()) for email in email_request.to_recipients.split(",")]
        
        cc_list = None
        if email_request.cc_recipients:
            cc_list = [EmailRecipient(email=email.strip()) for email in email_request.cc_recipients.split(",")]
        
        bcc_list = None
        if email_request.bcc_recipients:
            bcc_list = [EmailRecipient(email=email.strip()) for email in email_request.bcc_recipients.split(",")]
        
        # Aplicar variables a la plantilla
        if email_request.template_variables:
            for key, value in email_request.template_variables.items():
                template_content = template_content.replace(f"{{{key}}}", str(value))
        
        # Crear solicitud de correo
        email_request_obj = EmailRequest(
            subject=email_request.subject,
            body=template_content,
            body_type="HTML",
            to_recipients=to_list,
            cc_recipients=cc_list,
            bcc_recipients=bcc_list,
            importance=email_request.importance,
            attachments=email_request.attachments,
            template_variables=email_request.template_variables
        )
        
        # Enviar correo
        result = await email_service.send_email(email_request_obj)
        if not result.success:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": result.message}
            )
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al enviar correo desde plantilla: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al enviar correo desde plantilla: {str(e)}")