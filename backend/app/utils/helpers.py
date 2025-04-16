import json
import logging
from typing import Dict, List, Optional, Union, Any

logger = logging.getLogger(__name__)

def parse_comma_separated_emails(emails_str: str) -> List[str]:
    """
    Convierte una cadena de correos separados por comas en una lista de correos
    
    Args:
        emails_str: Cadena de correos separados por comas
    
    Returns:
        List[str]: Lista de direcciones de correo
    """
    if not emails_str:
        return []
    
    # Dividir por comas y eliminar espacios en blanco
    emails = [email.strip() for email in emails_str.split(',')]
    # Filtrar correos vacíos
    emails = [email for email in emails if email]
    
    return emails

def safe_json_loads(json_str: str) -> Optional[Dict[str, Any]]:
    """
    Intenta cargar un JSON desde una cadena de texto de forma segura
    
    Args:
        json_str: Cadena de texto JSON
    
    Returns:
        Optional[Dict[str, Any]]: Diccionario con el contenido JSON, o None si hubo un error
    """
    if not json_str:
        return None
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON: {str(e)}")
        return None

def apply_template_variables(content: str, variables: Dict[str, Any]) -> str:
    """
    Aplica variables a una plantilla
    
    Args:
        content: Contenido de la plantilla
        variables: Diccionario con las variables a aplicar
    
    Returns:
        str: Contenido con las variables aplicadas
    """
    if not variables:
        return content
    
    result = content
    for key, value in variables.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, str(value))
    
    return result

def format_size_human_readable(size_bytes: int) -> str:
    """
    Convierte un tamaño en bytes a una cadena legible para humanos
    
    Args:
        size_bytes: Tamaño en bytes
    
    Returns:
        str: Tamaño en formato legible (ej: "2.5 MB")
    """
    # Definimos las unidades
    units = ["B", "KB", "MB", "GB", "TB"]
    
    # Si el tamaño es 0, devolvemos "0 B"
    if size_bytes == 0:
        return "0 B"
    
    # Calculamos el logaritmo en base 1024
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    
    # Nos aseguramos de no pasarnos de las unidades disponibles
    if i >= len(units):
        i = len(units) - 1
    
    # Calculamos el valor
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {units[i]}"

def validate_email_address(email: str) -> bool:
    """
    Valida que una dirección de correo tenga un formato válido
    
    Args:
        email: Dirección de correo a validar
    
    Returns:
        bool: True si la dirección tiene un formato válido, False en caso contrario
    """
    import re
    # Patrón básico para validar correos electrónicos
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))