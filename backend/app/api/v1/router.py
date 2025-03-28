from fastapi import APIRouter

from app.api.v1.endpoints import emails, templates, attachments

api_router = APIRouter()

# Incluir routers para cada recurso
api_router.include_router(emails.router, prefix="/emails", tags=["Correos"])
api_router.include_router(templates.router, prefix="/templates", tags=["Plantillas"])
api_router.include_router(attachments.router, prefix="/attachments", tags=["Adjuntos"])