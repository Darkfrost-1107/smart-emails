import os
from pathlib import Path
from pydantic_settings import BaseSettings # type: ignore
from functools import lru_cache
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Definir rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
ATTACHMENTS_DIR = BASE_DIR / "attachments"
LOGS_DIR = BASE_DIR / "logs"

# Crear directorios si no existen
TEMPLATES_DIR.mkdir(exist_ok=True)
ATTACHMENTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

class Settings(BaseSettings):
    # Información de la aplicación
    APP_NAME: str = "API de Envío de Correos"
    API_V1_STR: str = "/api"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend para envío de correos utilizando Microsoft Graph API"
    
    # Microsoft Graph API
    MS_GRAPH_ENDPOINT: str = "https://graph.microsoft.com/v1.0"
    APPLICATION_ID: str = os.getenv("APPLICATION_ID", "")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "")
    TENANT_ID: str = os.getenv("TENANT_ID", "consumers")
    SCOPES: list = ["Mail.ReadWrite", "Mail.Send", "User.Read"]
    
    # Configuración de CORS
    CORS_ORIGINS: list = ["*"]
    
    # Configuración de log
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths
    TEMPLATES_DIR: Path = TEMPLATES_DIR
    ATTACHMENTS_DIR: Path = ATTACHMENTS_DIR
    LOGS_DIR: Path = LOGS_DIR
    
    # Limitaciones
    MAX_ATTACHMENT_SIZE: int = 10 * 1024 * 1024  # 10 MB
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    """Devuelve las configuraciones de la aplicación cacheadas"""
    return Settings()