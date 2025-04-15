from fastapi import Depends, HTTPException
from typing import Dict

from app.core.email_service import EmailService
from app.core.template_service import TemplateService
from app.core.attachment_service import AttachmentService

# Singleton services
_auth_service = None
_email_service = None
_template_service = None
_attachment_service = None

# def get_auth_service() ->EmailService:
#     """Obtiene el servicio de autenticación como dependencia"""
#     global _auth_service
#     if _auth_service is None:
#         _auth_service = EmailService()
#     return _auth_service

# def get_auth_headers(auth_service: EmailService = Depends(get_auth_service)) -> Dict[str, str]:
#     """Obtiene los encabezados de autenticación como dependencia"""
#     try:
#         return auth_service.get_auth_headers()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error de autenticación: {str(e)}")

def get_email_service() -> EmailService:
    """Obtiene el servicio de correo como dependencia"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service

def get_template_service() -> TemplateService:
    """Obtiene el servicio de plantillas como dependencia"""
    global _template_service
    if _template_service is None:
        _template_service = TemplateService()
    return _template_service

def get_attachment_service() -> AttachmentService:
    """Obtiene el servicio de adjuntos como dependencia"""
    global _attachment_service
    if _attachment_service is None:
        _attachment_service = AttachmentService()
    return _attachment_service