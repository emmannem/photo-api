# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import contact
from database import engine, Base
import uvicorn

# Inicializar la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Contacto",
    description="API para manejar formularios de contacto y enviar correos de confirmación",
    version="1.0.0",
)

# Configuración de CORS: Permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    allow_headers=["*"],  # Permitir todas las cabeceras
)

# Incluir las rutas del formulario de contacto
app.include_router(contact.router)

# Ruta de prueba básica


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Contacto"}


# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
