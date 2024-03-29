from fastapi import FastAPI
from routes.coche import coche
from routes.marcaCoche import marcaCoche
from routes.imagenCoche import imagenCoche
from routes.usuario import usuario
from routes.modeloCoche import modeloCoche
from config.openapi import tags_metadata
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de concesionario GMC",
    description="API para gestión de concesionario GMC",
    version="1.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

app.include_router(coche)
app.include_router(marcaCoche)
app.include_router(imagenCoche)
app.include_router(usuario)
app.include_router(modeloCoche)