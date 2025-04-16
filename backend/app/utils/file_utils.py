import os
import base64
import mimetypes
from pathlib import Path
from typing import List, Optional, Tuple

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Valida que un archivo tenga una extensión permitida
    
    Args:
        filename: Nombre del archivo a validar
        allowed_extensions: Lista de extensiones permitidas (sin punto inicial)
    
    Returns:
        bool: True si la extensión es válida, False en caso contrario
    """
    if not filename or '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions

def get_file_info(file_path: Path) -> Tuple[str, int, str]:
    """
    Obtiene información de un archivo
    
    Args:
        file_path: Ruta al archivo
    
    Returns:
        Tuple[str, int, str]: Tipo MIME, tamaño en bytes, fecha de modificación
    """
    from datetime import datetime
    
    mime_type = mimetypes.guess_type(file_path.name)[0] or 'application/octet-stream'
    size = file_path.stat().st_size
    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
    
    return mime_type, size, modified_time

def encode_file_to_base64(file_path: Path) -> Optional[str]:
    """
    Codifica un archivo a base64
    
    Args:
        file_path: Ruta al archivo
    
    Returns:
        Optional[str]: Contenido del archivo codificado en base64, o None si el archivo no existe
    """
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return base64.b64encode(content).decode('utf-8')
    except Exception:
        return None

def create_directory_if_not_exists(directory_path: Path) -> bool:
    """
    Crea un directorio si no existe
    
    Args:
        directory_path: Ruta al directorio
    
    Returns:
        bool: True si el directorio existe o fue creado correctamente, False en caso contrario
    """
    try:
        directory_path.mkdir(exist_ok=True, parents=True)
        return True
    except Exception:
        return False

def get_safe_filename(filename: str) -> str:
    """
    Obtiene un nombre de archivo seguro, eliminando caracteres problemáticos
    
    Args:
        filename: Nombre de archivo original
    
    Returns:
        str: Nombre de archivo seguro
    """
    import re
    # Reemplazar caracteres no alfanuméricos (excepto puntos, guiones y guiones bajos) con guiones bajos
    safe_name = re.sub(r'[^\w\-\.]', '_', filename)
    # Eliminar múltiples guiones bajos consecutivos
    safe_name = re.sub('_+', '_', safe_name)
    return safe_name