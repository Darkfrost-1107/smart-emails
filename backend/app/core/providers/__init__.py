from app.config import get_settings
from app.core.providers.base import BaseEmailProvider
from app.core.providers.titan.email_provider import TitanEmailProvider
from app.core.providers.outlook.email_provider import OutlookEmailProvider

def get_email_provider() -> BaseEmailProvider:
    """
    Factory function para obtener el proveedor de correo configurado.
    
    Returns:
        BaseEmailProvider: Implementación del proveedor de correo según configuración
    """
    settings = get_settings()
    provider_name = settings.EMAIL_PROVIDER.lower()
    
    if provider_name == "titan":
        return TitanEmailProvider()
    elif provider_name == "outlook":
        return OutlookEmailProvider()
    else:
        # Por defecto, usar Titan como proveedor
        return TitanEmailProvider()