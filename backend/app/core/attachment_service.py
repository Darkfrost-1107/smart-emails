import os
import logging
import mimetypes
import base64
from pathlib import Path
from typing import List
from datetime import datetime

from app.config import get_settings
from app.schemas.attachment import AttachmentInfo, AttachmentListResponse

settings = get_settings()
logger = logging.getLogger(__name__)

class AttachmentService:
    """Servicio para la gestión de archivos adjuntos"""
    
    def __init__(self):
        self.attachments_dir = settings.ATTACHMENTS_DIR
        # Asegurar que el directorio existe
        self.attachments_dir.mkdir(exist_ok=True)
    
    def list_attachments(self) -> AttachmentListResponse:
        """Lista todos los archivos adjuntos disponibles"""
        attachments = []
        
        for file_path in self.attachments_dir.glob("*"):
            if file_path.is_file():
                # Obtener tipo MIME
                mime_type = mimetypes.guess_type(file_path.name)[0] or 'application/octet-stream'
                
                # Obtener estadísticas del archivo
                stats = file_path.stat()
                attachment_info = AttachmentInfo(
                    filename=file_path.name,
                    content_type=mime_type,
                    size=stats.st_size,
                    path=str(file_path.relative_to(settings.BASE_DIR))
                )
                attachments.append(attachment_info)
        
        return AttachmentListResponse(attachments=attachments)
    
    def save_attachment(self, filename: str, content: bytes) -> AttachmentInfo:
        """Guarda un nuevo archivo adjunto"""
        # Verificar tamaño
        if len(content) > settings.MAX_ATTACHMENT_SIZE:
            logger.warning(f"Archivo adjunto demasiado grande: {filename} ({len(content)} bytes)")
            raise ValueError(f"El archivo excede el tamaño máximo permitido ({settings.MAX_ATTACHMENT_SIZE} bytes)")
        
        file_path = self.attachments_dir / filename
        
        try:
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Obtener tipo MIME
            mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            
            # Obtener estadísticas actualizadas
            stats = file_path.stat()
            return AttachmentInfo(
                filename=filename,
                content_type=mime_type,
                size=stats.st_size,
                path=str(file_path.relative_to(settings.BASE_DIR))
            )
        except Exception as e:
            logger.exception(f"Error al guardar archivo adjunto {filename}: {str(e)}")
            raise
    
    def delete_attachment(self, filename: str) -> bool:
        """Elimina un archivo adjunto existente"""
        file_path = self.attachments_dir / filename
        
        if not file_path.exists():
            logger.warning(f"Intento de eliminar archivo inexistente: {filename}")
            return False
        
        try:
            file_path.unlink()
            logger.info(f"Archivo adjunto eliminado: {filename}")
            return True
        except Exception as e:
            logger.exception(f"Error al eliminar archivo adjunto {filename}: {str(e)}")
            raise
    
    def get_attachment_content(self, filename: str) -> bytes:
        """Obtiene el contenido de un archivo adjunto"""
        file_path = self.attachments_dir / filename
        
        if not file_path.exists():
            logger.error(f"Archivo adjunto no encontrado: {filename}")
            raise FileNotFoundError(f"Archivo adjunto '{filename}' no encontrado")
        
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            logger.exception(f"Error al leer archivo adjunto {filename}: {str(e)}")
            raise
    
    def get_attachment_as_base64(self, filename: str) -> str:
        """Obtiene el contenido de un archivo adjunto en formato Base64"""
        content = self.get_attachment_content(filename)
        return base64.b64encode(content).decode('utf-8')
    
    def create_attachment_dict(self, filename: str) -> dict:
        """Crea un diccionario con la información del adjunto para Microsoft Graph API"""
        content = self.get_attachment_content(filename)
        mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        return {
            '@odata.type': '#microsoft.graph.fileAttachment',
            'name': filename,
            'contentType': mime_type,
            'contentBytes': base64.b64encode(content).decode('utf-8')
        }