import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import get_settings
from app.api.v1.router import api_router

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path("logs/app.log"))
    ]
)

settings = get_settings()

def create_application() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI
    """
    application = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configurar CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Incluir rutas de la API
    application.include_router(api_router, prefix=settings.API_V1_STR)

    # Montar directorios estáticos
    static_dir = Path("static")
    if static_dir.exists():
        application.mount("/static", StaticFiles(directory=static_dir), name="static")

    @application.get("/", tags=["Status"])
    async def root():
        """Verificar estado de la API"""
        return {
            "status": "online",
            "app_name": settings.APP_NAME,
            "version": settings.VERSION
        }

    @application.get("/health", tags=["Status"])
    async def health_check():
        """Verificar salud de la aplicación"""
        return {"status": "healthy"}

    return application