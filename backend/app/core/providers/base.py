from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from app.schemas.email import EmailRequest, EmailResponse, Attachment

class BaseEmailProvider(ABC):
    """
    Interfaz base para los proveedores de servicios de correo electrónico.
    Todas las implementaciones específicas deben heredar de esta clase.
    """
    
    @abstractmethod
    async def send_email(self, email_data: EmailRequest) -> EmailResponse:
        """
        Envía un correo electrónico usando el proveedor específico.
        
        Args:
            email_data: Datos del correo a enviar
            
        Returns:
            EmailResponse: Resultado del envío
        """
        pass
    
    @abstractmethod
    def process_attachments(self, attachments: List[Attachment]) -> Any:
        """
        Procesa los archivos adjuntos en el formato requerido por el proveedor.
        
        Args:
            attachments: Lista de archivos adjuntos
            
        Returns:
            Any: Representación de los adjuntos en el formato del proveedor
        """
        pass