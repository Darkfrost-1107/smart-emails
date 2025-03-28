from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field

class EmailRecipient(BaseModel):
    """Modelo para un destinatario de correo electrónico"""
    email: EmailStr
    name: Optional[str] = None

class Attachment(BaseModel):
    """Modelo para un archivo adjunto"""
    filename: str
    content_type: Optional[str] = None
    content: str  # Base64 encoded content

class EmailRequest(BaseModel):
    """Modelo para una solicitud de envío de correo electrónico"""
    subject: str
    body: str
    body_type: str = "HTML"  # "HTML" o "Text"
    to_recipients: List[EmailRecipient]
    cc_recipients: Optional[List[EmailRecipient]] = None
    bcc_recipients: Optional[List[EmailRecipient]] = None
    importance: str = "normal"  # "low", "normal", "high"
    attachments: Optional[List[Attachment]] = None
    save_to_sent_items: bool = True
    template_variables: Optional[Dict[str, Any]] = None

class EmailResponse(BaseModel):
    """Modelo para una respuesta de envío de correo electrónico"""
    success: bool
    message: str
    email_id: Optional[str] = None

class TemplateEmailRequest(BaseModel):
    """Modelo para una solicitud de envío de correo electrónico usando una plantilla"""
    template_name: str
    subject: str
    to_recipients: str  # Lista de emails separados por coma
    cc_recipients: Optional[str] = None
    bcc_recipients: Optional[str] = None
    importance: str = "normal"
    template_variables: Optional[Dict[str, Any]] = None
    save_to_sent_items: bool = True