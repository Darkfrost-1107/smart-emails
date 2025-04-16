# API de Envío de Correos con FastAPI

API RESTful para el envío de correos utilizando Microsoft Graph API, con soporte para plantillas HTML y archivos adjuntos.

## Características

- Envío de correos utilizando Microsoft Graph API
- Gestión de plantillas HTML con variables
- Gestión de archivos adjuntos
- Soporte para diferentes tipos de destinatarios (principal, copia, copia oculta)
- Documentación automática con Swagger UI
- Estructura modular y escalable

## Requisitos

- Python 3.8 o superior
- Cuenta de Microsoft y registro de aplicación en Azure Portal

## Estructura del Proyecto

```
email-api/
│
├── .env                           # Variables de entorno
├── main.py                        # Punto de entrada principal
├── requirements.txt               # Dependencias del proyecto
│
├── app/                           # Código principal de la aplicación
│   ├── __init__.py                # Inicialización del módulo
│   ├── config.py                  # Configuración de la aplicación
│   ├── core/                      # Núcleo de la aplicación
│   │   ├── __init__.py
│   │   ├── auth.py                # Módulo de autenticación
│   │   ├── email_service.py       # Servicio de envío de correos
│   │   ├── template_service.py    # Servicio de gestión de plantillas
│   │   └── attachment_service.py  # Servicio de gestión de adjuntos
│   │
│   ├── api/                       # Rutas de la API
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependencias de la API
│   │   ├── v1/                    # Versión 1 de la API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/         # Endpoints de la API
│   │   │   │   ├── __init__.py
│   │   │   │   ├── emails.py      # Endpoints para correos
│   │   │   │   ├── templates.py   # Endpoints para plantillas
│   │   │   │   └── attachments.py # Endpoints para adjuntos
│   │   │   └── router.py          # Router principal v1
│   │   └── api.py                 # Configuración de la API
│   │
│   ├── schemas/                   # Modelos Pydantic
│   │   ├── __init__.py
│   │   ├── email.py               # Esquemas para correos
│   │   ├── template.py            # Esquemas para plantillas
│   │   └── attachment.py          # Esquemas para adjuntos
│   │
│   └── utils/                     # Utilidades
│       ├── __init__.py
│       ├── file_utils.py          # Utilidades para archivos
│       └── helpers.py             # Funciones auxiliares
│
├── templates/                     # Directorio para plantillas HTML
│   └── notificacion.html          # Ejemplo de plantilla
│
├── attachments/                   # Directorio para adjuntos
│   └── .gitkeep                   # Para mantener el directorio en git
│
├── logs/                          # Directorio para logs
│   └── .gitkeep
│
└── static/                        # Archivos estáticos
    └── docs/                      # Documentación
        └── index.html             # Página principal de documentación
```

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/email-api.git
cd email-api
```

2. Crea un entorno virtual y actívalo:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
APPLICATION_ID=tu_application_id
CLIENT_SECRET=tu_client_secret
TENANT_ID=consumers
```

Donde `APPLICATION_ID` y `CLIENT_SECRET` son las credenciales de tu aplicación registrada en Azure Portal.

## Ejecución

1. Inicia el servidor:

```bash
uvicorn main:app --reload
```

2. Abre la documentación Swagger UI:

Navega a `http://localhost:8000/docs` en tu navegador.

## Guía de Uso

### Envío de Correo Simple

```python
import requests
import json

# Datos del correo
data = {
    "subject": "Prueba de correo",
    "body": "<h1>Hola mundo</h1><p>Este es un correo de prueba.</p>",
    "body_type": "HTML",
    "to_recipients": [
        {"email": "destinatario@ejemplo.com", "name": "Nombre Destinatario"}
    ],
    "cc_recipients": [
        {"email": "copia@ejemplo.com", "name": "Copia"}
    ],
    "importance": "high",
    "save_to_sent_items": True
}

# Enviar solicitud
response = requests.post(
    "http://localhost:8000/api/emails/send",
    json=data
)

print(response.json())
```

### Envío de Correo con Plantilla

1. Primero, sube una plantilla HTML:

```python
import requests

files = {'template_file': ('plantilla.html', open('plantilla.html', 'rb'), 'text/html')}
data = {'template_name': 'mi_plantilla'}

response = requests.post(
    "http://localhost:8000/api/templates/upload",
    files=files,
    data=data
)

print(response.json())
```

2. Luego, envía un correo utilizando la plantilla:

```python
import requests
import json

# Datos del formulario
data = {
    "template_name": "mi_plantilla",
    "subject": "Correo con plantilla",
    "to_recipients": "destinatario@ejemplo.com",
    "cc_recipients": "copia@ejemplo.com",
    "importance": "normal",
    "template_variables": json.dumps({
        "nombre": "Juan Pérez",
        "empresa": "Mi Empresa S.A.",
        "fecha": "2025-03-28"
    })
}

# Archivos adjuntos (opcional)
files = [
    ('files', ('documento.pdf', open('documento.pdf', 'rb'), 'application/pdf'))
]

# Enviar solicitud
response = requests.post(
    "http://localhost:8000/api/emails/send-template",
    data=data,
    files=files
)

print(response.json())
```

## Endpoints Principales

### Correos

- `POST /api/emails/send` - Envía un correo electrónico
- `POST /api/emails/send-template` - Envía un correo utilizando una plantilla HTML

### Plantillas

- `GET /api/templates` - Lista todas las plantillas disponibles
- `GET /api/templates/{template_name}` - Obtiene una plantilla específica
- `POST /api/templates/upload` - Sube una nueva plantilla
- `DELETE /api/templates/{template_name}` - Elimina una plantilla
- `POST /api/templates/preview` - Previsualiza una plantilla con variables

### Adjuntos

- `GET /api/attachments` - Lista todos los archivos adjuntos disponibles
- `POST /api/attachments/upload` - Sube un nuevo archivo adjunto
- `GET /api/attachments/{filename}` - Descarga un archivo adjunto
- `DELETE /api/attachments/{filename}` - Elimina un archivo adjunto

## Licencia

[MIT](LICENSE)