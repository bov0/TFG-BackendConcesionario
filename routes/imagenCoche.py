from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from schemas.ImagenCoche import ImagenCocheBase
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
def create_imagenCoche(imagen_coche_data: ImagenCocheBase):
    nuevaImagen = {
        "coche_id": imagen_coche_data.coche_id,
        "imagen": imagen_coche_data.imagen
    }

    result = conn.execute(ImagenCocheBase.insert().values(nuevaImagen))
    nuevaImagen["id"] = result.lastrowid
    return nuevaImagen

@imagenCoche.put(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    description="Modificar imagen de coche por ID"
)
def update_imagen_coche(imagen_coche_data: ImagenCocheBase, id: int):
    # Verificar si la imagen de coche con el ID proporcionado existe
    imagenExistente = conn.execute(select(ImagenCocheBase).where(ImagenCocheBase.c.id == id)).first()
    if imagenExistente is None:
        raise HTTPException(status_code=404, detail="No existe ninguna imagen de coche con el ID proporcionado")

    conn.execute(
        ImagenCocheBase.update()
        .values(
            coche_id=imagen_coche_data.coche_id,
            imagen=imagen_coche_data.imagen
        )
        .where(ImagenCocheBase.c.id == id)
    )

    return conn.execute(select(ImagenCocheBase).where(ImagenCocheBase.c.id == id)).first()

@imagenCoche.delete(
    "/imagenes-coche/{id}",
    response_model=ImagenCocheBase,
    tags=["imagenes-coche"],
    description="Eliminar una imagen de coche por ID"
)
def delete_imagenCoche(id: int):
    imagenEliminada = conn.execute(ImagenCocheBase.delete().where(ImagenCocheBase.c.id == id)).first()
    return imagenEliminada
