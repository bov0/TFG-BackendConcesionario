from fastapi import FastAPI
from routes import coche, marcaCoche, imagenCoche, usuario
from config.openapi import tags_metadata

app = FastAPI(
    title="API de animales",
    description="API para gestión de concesionario GMC",
    version="1.0",
    openapi_tags=tags_metadata,
)

app.include_router(coche)
app.include_router(marcaCoche)
app.include_router(imagenCoche)
app.include_router(usuario)