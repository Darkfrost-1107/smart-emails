import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

from app.config import get_settings
from app.schemas.template import TemplateInfo, TemplateListResponse

settings = get_settings()
logger = logging.getLogger(__name__)

class TemplateService:
    """Servicio para la gestión de plantillas HTML"""
    
    def __init__(self):
        self.templates_dir = settings.TEMPLATES_DIR
        # Asegurar que el directorio existe
        self.templates_dir.mkdir(exist_ok=True)
    
    def list_templates(self) -> TemplateListResponse:
        """Lista todas las plantillas disponibles"""
        templates = []
        
        for file_path in self.templates_dir.glob("*.html"):
            if file_path.is_file():
                # Obtener estadísticas del archivo
                stats = file_path.stat()
                template_info = TemplateInfo(
                    name=file_path.stem,
                    path=str(file_path.relative_to(settings.BASE_DIR)),
                    size=stats.st_size,
                    last_modified=datetime.fromtimestamp(stats.st_mtime).isoformat()
                )
                templates.append(template_info)
        
        return TemplateListResponse(templates=templates)
    
    def get_template_content(self, template_name: str) -> str:
        """Obtiene el contenido de una plantilla"""
        template_path = self.templates_dir / f"{template_name}.html"
        
        if not template_path.exists():
            logger.error(f"Plantilla no encontrada: {template_name}")
            raise FileNotFoundError(f"Plantilla '{template_name}' no encontrada")
        
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.exception(f"Error al leer la plantilla {template_name}: {str(e)}")
            raise
    
    def save_template(self, template_name: str, content: bytes) -> TemplateInfo:
        """Guarda una nueva plantilla o actualiza una existente"""
        template_path = self.templates_dir / f"{template_name}.html"
        
        try:
            with open(template_path, "wb") as f:
                f.write(content)
            
            # Obtener estadísticas actualizadas
            stats = template_path.stat()
            return TemplateInfo(
                name=template_name,
                path=str(template_path.relative_to(settings.BASE_DIR)),
                size=stats.st_size,
                last_modified=datetime.fromtimestamp(stats.st_mtime).isoformat()
            )
        except Exception as e:
            logger.exception(f"Error al guardar la plantilla {template_name}: {str(e)}")
            raise
    
    def delete_template(self, template_name: str) -> bool:
        """Elimina una plantilla existente"""
        template_path = self.templates_dir / f"{template_name}.html"
        
        if not template_path.exists():
            logger.warning(f"Intento de eliminar plantilla inexistente: {template_name}")
            return False
        
        try:
            template_path.unlink()
            logger.info(f"Plantilla eliminada: {template_name}")
            return True
        except Exception as e:
            logger.exception(f"Error al eliminar la plantilla {template_name}: {str(e)}")
            raise
    
    def render_template(self, template_name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Renderiza una plantilla con variables"""
        content = self.get_template_content(template_name)
        
        # Aplicar variables si están disponibles
        if variables:
            for key, value in variables.items():
                content = content.replace(f"{{{key}}}", str(value))
        
        return content