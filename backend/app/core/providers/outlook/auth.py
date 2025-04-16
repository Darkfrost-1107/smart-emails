import os
import logging
from pathlib import Path
import msal
from fastapi import HTTPException

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class OutlookAuth:
    """Clase para manejar la autenticación con Microsoft Graph API para Outlook"""
    
    def __init__(self):
        self.application_id = settings.APPLICATION_ID
        self.client_secret = settings.CLIENT_SECRET
        self.tenant_id = settings.TENANT_ID
        self.scopes = settings.SCOPES
        self.refresh_token_path = Path(settings.BASE_DIR / "refresh_token.txt")
    
    def get_access_token(self):
        """Obtiene un token de acceso para Microsoft Graph API"""
        try:
            client = msal.ConfidentialClientApplication(
                client_id=self.application_id,
                client_credential=self.client_secret,
                authority=f'https://login.microsoftonline.com/{self.tenant_id}/'
            )
            
            # Intentar usar un refresh token si existe
            refresh_token = None
            if self.refresh_token_path.exists():
                with open(self.refresh_token_path, 'r') as f:
                    refresh_token = f.read().strip()
            
            if refresh_token:
                logger.info("Intentando obtener token con refresh token")
                token_response = client.acquire_token_by_refresh_token(refresh_token, self.scopes)
                if 'access_token' in token_response:
                    if 'refresh_token' in token_response:
                        with open(self.refresh_token_path, 'w') as f:
                            f.write(token_response['refresh_token'])
                    logger.info("Token obtenido correctamente con refresh token")
                    return token_response['access_token']
                else:
                    logger.warning("No se pudo obtener token con refresh token. Error: %s", 
                                  token_response.get('error_description', 'Unknown error'))
            
            # Si no hay refresh token o falló, usamos credenciales de cliente (sin interacción del usuario)
            logger.info("Intentando obtener token con credenciales de cliente")
            token_response = client.acquire_token_for_client(scopes=self.scopes)
            
            if 'access_token' in token_response:
                logger.info("Token obtenido correctamente con credenciales de cliente")
                return token_response['access_token']
            else:
                error_message = token_response.get('error_description', 'Unknown error')
                logger.error("Error al obtener token: %s", error_message)
                raise HTTPException(status_code=401, detail=f"Error acquiring token: {error_message}")
                
        except Exception as e:
            logger.exception("Error en el proceso de autenticación")
            raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

    def get_auth_headers(self):
        """Obtiene los encabezados de autorización para las solicitudes a Microsoft Graph API"""
        access_token = self.get_access_token()
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }