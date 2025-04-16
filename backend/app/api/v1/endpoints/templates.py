import json
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse

from app.schemas.template import TemplateListResponse, TemplateUploadResponse, TemplatePreviewRequest
from app.core.template_service import TemplateService
from app.api.deps import get_template_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=TemplateListResponse)
async def list_templates(
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Lista todas las plantillas HTML disponibles.
    """
    try:
        return template_service.list_templates()
    except Exception as e:
        logger.exception(f"Error al listar plantillas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al listar plantillas: {str(e)}")

@router.get("/{template_name}", response_class=HTMLResponse)
async def get_template(
    template_name: str,
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Obtiene el contenido de una plantilla HTML específica.
    """
    try:
        return template_service.get_template_content(template_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Plantilla '{template_name}' no encontrada")
    except Exception as e:
        logger.exception(f"Error al obtener plantilla {template_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener plantilla: {str(e)}")

@router.post("/upload", response_model=TemplateUploadResponse)
async def upload_template(
    template_name: str = Form(...),
    template_file: UploadFile = File(...),
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Sube una nueva plantilla HTML o actualiza una existente.
    """
    try:
        # Verificar extensión
        if not template_file.filename.endswith(".html"):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos HTML")
        
        # Leer contenido
        content = await template_file.read()
        
        # Guardar plantilla
        template_info = template_service.save_template(template_name, content)
        
        return TemplateUploadResponse(
            success=True,
            message=f"Plantilla '{template_name}' subida correctamente",
            template=template_info
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al subir plantilla: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al subir plantilla: {str(e)}")

@router.delete("/{template_name}")
async def delete_template(
    template_name: str,
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Elimina una plantilla existente.
    """
    try:
        success = template_service.delete_template(template_name)
        if not success:
            raise HTTPException(status_code=404, detail=f"Plantilla '{template_name}' no encontrada")
        
        return {"success": True, "message": f"Plantilla '{template_name}' eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al eliminar plantilla {template_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar plantilla: {str(e)}")

@router.post("/preview", response_class=HTMLResponse)
async def preview_template(
    preview_data: TemplatePreviewRequest,
    template_service: TemplateService = Depends(get_template_service)
):
    """
    Previsualiza una plantilla con variables aplicadas.
    """
    try:
        return template_service.render_template(
            preview_data.template_name,
            preview_data.template_variables
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Plantilla '{preview_data.template_name}' no encontrada")
    except Exception as e:
        logger.exception(f"Error al previsualizar plantilla: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al previsualizar plantilla: {str(e)}")