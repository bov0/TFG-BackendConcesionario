from fastapi import APIRouter, HTTPException, Form, UploadFile
from sqlalchemy import select
from schemas.ImagenCoche import ImagenCocheBase
from schemas.Coche import CocheBase
from config.db import conn

imagenCoche = APIRouter()

@imagenCoche.get(
    "/imagenes-coche",
    tags=["imagenes-coche"],
    response_model=list[ImagenCocheBase],
    description="Lista de todas las imágenes de coche"
)
def get_imagenes_coche():
    return conn.execute(select(ImagenCocheBase)).fetchall()

@imagenCoche.get(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Ver imagen de coche por ID único"
)
def get_imagen_coche(id: int):
    imagenCoche = conn.execute(select(ImagenCocheBase).where(ImagenCocheBase.c.id == id)).first()
    if imagenCoche is None:
        raise HTTPException(status_code=404, detail="Imagen de coche no encontrada")
    return imagenCoche

@imagenCoche.post(
    "/imagenes-coche",
    response_model=ImagenCocheBase,
    status_code=201,
    tags=["imagenes-coche"],
    description="Subir una nueva imagen de coche"
)
async def create_imagenCoche(
    coche_id: int = Form(..., title="ID del Coche", description="ID del coche al que pertenece la imagen"),
    imagen_coche: UploadFile = Form(..., title="Imagen del Coche", description="Imagen del coche en formato de archivo")
):
    # Verificar si ya existe un coche con ese ID
    existeCoche = conn.execute(select(CocheBase).where(CocheBase.c.id == coche_id)).first()
    
    if existeCoche:
        imagen_blob = await imagen_coche.read()

        nueva_imagen = {
            "coche_id": coche_id,
            "imagen": imagen_blob
        }

        result = conn.execute(ImagenCocheBase.insert().values(nueva_imagen))
        nueva_imagen["id"] = result.lastrowid
        return nueva_imagen
    else:
        raise HTTPException(status_code=400, detail="No existe un coche con este ID")

@imagenCoche.put(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Modificar imagen de coche por ID"
)
async def update_imagen_coche(
    id: int,
    coche_id: int = Form(..., title="ID del Coche", description="ID del coche al que pertenece la imagen"),
    imagen_coche: UploadFile = Form(..., title="Imagen del Coche", description="Imagen del coche en formato de archivo")
):
    # Verificar si la imagen de coche con el ID proporcionado existe
    imagenExistente = conn.execute(select(ImagenCocheBase).where(ImagenCocheBase.c.id == id)).first()
    if imagenExistente is None:
        raise HTTPException(status_code=404, detail="No existe ninguna imagen de coche con el ID proporcionado")

    # Verificar si ya existe un coche con ese ID
    existeCoche = conn.execute(select(CocheBase).where(CocheBase.c.id == coche_id)).first()
    if existeCoche:
        imagen_blob = await imagen_coche.read()

        conn.execute(
            ImagenCocheBase.update()
            .values(
                coche_id=coche_id,
                imagen=imagen_blob
            )
            .where(ImagenCocheBase.c.id == id)
        )

        return conn.execute(select(ImagenCocheBase).where(ImagenCocheBase.c.id == id)).first()
    else:
        raise HTTPException(status_code=400, detail="No existe un coche con este ID")

@imagenCoche.delete(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Eliminar una imagen de coche por ID"
)
def delete_imagenCoche(id: int):
    imagenEliminada = conn.execute(ImagenCocheBase.delete().where(ImagenCocheBase.c.id == id)).first()
    return imagenEliminada
