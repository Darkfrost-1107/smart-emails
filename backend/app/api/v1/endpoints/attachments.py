import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response

from app.schemas.attachment import AttachmentListResponse, AttachmentUploadResponse
from app.core.attachment_service import AttachmentService
from app.config import get_settings
from app.api.deps import get_attachment_service

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()

@router.get("/", response_model=AttachmentListResponse)
async def list_attachments(
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    """
    Lista todos los archivos adjuntos disponibles.
    """
    try:
        return attachment_service.list_attachments()
    except Exception as e:
        logger.exception(f"Error al listar archivos adjuntos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al listar archivos adjuntos: {str(e)}")

@router.post("/upload", response_model=AttachmentUploadResponse)
async def upload_attachment(
    file: UploadFile = File(...),
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    """
    Sube un nuevo archivo para usar como adjunto.
    """
    try:
        # Leer contenido
        content = await file.read()
        
        # Verificar tamaño
        if len(content) > settings.MAX_ATTACHMENT_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"El archivo excede el tamaño máximo permitido ({settings.MAX_ATTACHMENT_SIZE} bytes)"
            )
        
        # Guardar archivo
        attachment_info = attachment_service.save_attachment(file.filename, content)
        
        return AttachmentUploadResponse(
            success=True,
            message=f"Archivo '{file.filename}' subido correctamente",
            attachment=attachment_info
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al subir archivo adjunto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al subir archivo adjunto: {str(e)}")

@router.get("/{filename}")
async def get_attachment(
    filename: str,
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    """
    Descarga un archivo adjunto.
    """
    try:
        content = attachment_service.get_attachment_content(filename)
        
        # Determinar el tipo MIME
        import mimetypes
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        return Response(
            content=content,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Archivo adjunto '{filename}' no encontrado")
    except Exception as e:
        logger.exception(f"Error al obtener archivo adjunto {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener archivo adjunto: {str(e)}")

@router.delete("/{filename}")
async def delete_attachment(
    filename: str,
    attachment_service: AttachmentService = Depends(get_attachment_service)
):
    """
    Elimina un archivo adjunto existente.
    """
    try:
        success = attachment_service.delete_attachment(filename)
        if not success:
            raise HTTPException(status_code=404, detail=f"Archivo adjunto '{filename}' no encontrado")
        
        return {
            "success": True,
            "message": f"Archivo adjunto '{filename}' eliminado correctamente",
            "filename": filename
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al eliminar archivo adjunto {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar archivo adjunto: {str(e)}")