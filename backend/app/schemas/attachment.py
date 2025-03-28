
from typing import List, Optional
from pydantic import BaseModel

class AttachmentInfo(BaseModel):
    """Información sobre un archivo adjunto"""
    filename: str
    content_type: str
    size: int
    path: str

class AttachmentListResponse(BaseModel):
    """Respuesta con la lista de archivos adjuntos disponibles"""
    attachments: List[AttachmentInfo]

class AttachmentUploadResponse(BaseModel):
    """Respuesta para la subida de un archivo adjunto"""
    success: bool
    message: str
    attachment: Optional[AttachmentInfo] = None

class AttachmentDeleteResponse(BaseModel):
    """Respuesta para la eliminación de un archivo adjunto"""
    success: bool
    message: str
    filename: str