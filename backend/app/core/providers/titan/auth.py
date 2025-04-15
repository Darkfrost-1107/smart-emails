import logging
from smtplib import SMTP
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class TitanAuth:
    """Clase para manejar la autenticación con Titan Email SMTP"""
    
    def __init__(self):
        self.smtp_server = settings.TITAN_SMTP_SERVER
        self.smtp_port = settings.TITAN_SMTP_PORT
        self.sender_email = settings.TITAN_SENDER_EMAIL
        self.sender_password = settings.TITAN_SENDER_PASSWORD
    
    def get_smtp_connection(self) -> SMTP:
        """
        Establece una conexión autenticada con el servidor SMTP de Titan
        
        Returns:
            SMTP: Conexión SMTP autenticada
        
        Raises:
            Exception: Si hay un error en la autenticación o conexión
        """
        try:
            logger.info(f"Conectando al servidor SMTP de Titan: {self.smtp_server}:{self.smtp_port}")
            
            # Crear la conexión SMTP
            smtp_conn = SMTP(self.smtp_server, self.smtp_port)
            
            # Iniciar TLS para conexión segura
            smtp_conn.starttls()
            
            # Autenticar con las credenciales
            logger.info(f"Autenticando con el usuario: {self.sender_email}")
            smtp_conn.login(self.sender_email, self.sender_password)
            
            logger.info("Conexión SMTP establecida correctamente")
            return smtp_conn
        
        except Exception as e:
            logger.exception(f"Error al establecer conexión SMTP: {str(e)}")
            raise