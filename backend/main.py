import uvicorn
from app.api.api import create_application

# Crear la aplicación FastAPI
app = create_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


