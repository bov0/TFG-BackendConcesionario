from fastapi import APIRouter, HTTPException, Form, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from schemas.ImagenCoche import ImagenCocheBase
from models.ImagenCoche import ImagenCoche
from models.Coche import Coche
from config.db import conn
import io

imagenCoche = APIRouter()

@imagenCoche.get(
    "/imagenes-coche",
    tags=["imagenes-coche"],
    response_model=list[ImagenCocheBase],
    description="Lista de todas las imágenes de coche"
)
async def get_imagenes_coche():
    return conn.execute(select(ImagenCoche)).fetchall()

@imagenCoche.get(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Ver imagen de coche por ID único"
)
async def get_imagen_coche(id: int):
    imagenCoche = conn.execute(select(ImagenCoche).where(ImagenCoche.c.id == id)).first()
    if imagenCoche is None:
        raise HTTPException(status_code=404, detail="Imagen de coche no encontrada")
    return imagenCoche

@imagenCoche.post(
    "/imagenes-coche",
    response_model=str,
    tags=["imagenes-coche"],
    description="Subir una nueva imagen de coche"
)
async def create_imagenCoche(
    coche_id: int = Form(..., title="ID del Coche", description="ID del coche al que pertenece la imagen"),
    imagen: UploadFile = UploadFile
):
    # Verificar si ya existe un coche con ese ID
    existeCoche = conn.execute(select(Coche).where(Coche.c.id == coche_id)).first()

    if existeCoche:
        imagen_blob = await imagen.read()

        nueva_imagen = {
            "coche_id": coche_id,
            "imagen": imagen_blob
        }

        result = conn.execute(ImagenCoche.insert().values(nueva_imagen))
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
    imagenExistente = conn.execute(select(ImagenCoche).where(ImagenCoche.c.id == id)).first()
    if imagenExistente is None:
        raise HTTPException(status_code=404, detail="No existe ninguna imagen de coche con el ID proporcionado")

    # Verificar si ya existe un coche con ese ID
    existeCoche = conn.execute(select(Coche).where(Coche.c.id == coche_id)).first()
    if existeCoche:
        imagen_blob = await imagen_coche.read()

        conn.execute(
            ImagenCoche.update()
            .values(
                coche_id=coche_id,
                imagen=imagen_blob
            )
            .where(ImagenCoche.c.id == id)
        )

        return conn.execute(select(ImagenCoche).where(ImagenCoche.c.id == id)).first()
    else:
        raise HTTPException(status_code=400, detail="No existe un coche con este ID")

@imagenCoche.delete(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Eliminar una imagen de coche por ID"
)
async def delete_imagenCoche(id: int):
    imagenEliminada = conn.execute(ImagenCoche.delete().where(ImagenCoche.c.id == id)).first()
    return "Imagen eliminada"

@imagenCoche.delete(
    "/imagenes-coche/byCar/{id}",
    tags=["imagenes-coche"],
    description="Eliminar una imagen de coche por ID de coche"
)
async def delete_imagenCoche_ByIdCoche(id: int):
    imagenEliminada = conn.execute(ImagenCoche.delete().where(ImagenCoche.c.coche_id == id)).first()
    return "Imagen eliminada"

@imagenCoche.get(
    "/imagenes-coche/imagen/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Ver una imagen de coche por ID del coche"
)
async def ver_imagenCoche(id: int):
    try:
        # Obtén la imagen de la base de datos por ID
        imagen_coche = conn.execute(select(ImagenCoche).where(ImagenCoche.c.coche_id == id)).first()

        if not imagen_coche:
            raise HTTPException(status_code=404, detail="Imagen de coche no encontrada")

        # Retorna la imagen como respuesta
        return StreamingResponse(io.BytesIO(imagen_coche.imagen), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar la imagen: {str(e)}")