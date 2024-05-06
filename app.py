from fastapi import FastAPI
from routes.coche import coche
from routes.marcaCoche import marcaCoche
from routes.imagenCoche import imagenCoche
from routes.usuario import usuario
from routes.modeloCoche import modeloCoche
<<<<<<< HEAD
from routes.cocheVendido import cocheVendido
from routes.venta import venta
=======
from routes.ventas import ventas
from routes.cochesVendidos import cocheVendido
>>>>>>> 3ba74ff5e3caba85aa2dc56bda2731574d5e3646
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
    allow_origins=["*", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

app.include_router(coche)
app.include_router(marcaCoche)
app.include_router(imagenCoche)
app.include_router(usuario)
app.include_router(modeloCoche)
<<<<<<< HEAD
app.include_router(cocheVendido)
app.include_router(venta)
=======
app.include_router(ventas)
app.include_router(cocheVendido)
>>>>>>> 3ba74ff5e3caba85aa2dc56bda2731574d5e3646
