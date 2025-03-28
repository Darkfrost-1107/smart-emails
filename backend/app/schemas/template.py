from typing import List, Optional
from pydantic import BaseModel

class TemplateInfo(BaseModel):
    """Información sobre una plantilla"""
    name: str
    path: str
    size: int
    last_modified: str

class TemplateListResponse(BaseModel):
    """Respuesta con la lista de plantillas disponibles"""
    templates: List[TemplateInfo]

class TemplateUploadResponse(BaseModel):
    """Respuesta para la subida de una plantilla"""
    success: bool
    message: str
    template: Optional[TemplateInfo] = None

class TemplatePreviewRequest(BaseModel):
    """Solicitud para previsualizar una plantilla con variables"""
    template_name: str
    template_variables: Optional[dict] = None