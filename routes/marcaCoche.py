from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from models.MarcaCoche import MarcaCoche
from schemas.MarcaCoche import MarcaCocheBase
from config.db import conn

marcaCoche = APIRouter()

@marcaCoche.get(
    "/marcas-coche",
    tags=["marcas-coche"],
    response_model=list[MarcaCocheBase],
    description="Lista de todas las marcas de coche"
)
def get_marcas_coche():
    return conn.execute(select(MarcaCoche)).fetchall()

@marcaCoche.get(
    "/marcas-coche/{id}",
    response_model=MarcaCocheBase,
    tags=["marcas-coche"],
    description="Ver marca de coche por ID único"
)
def get_marca_coche(id: int):
    marca_coche = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == id)).first()
    if marca_coche is None:
        raise HTTPException(status_code=404, detail="Marca de coche no encontrada")
    return marca_coche

@marcaCoche.post(
    "/marcas-coche",
    response_model=MarcaCocheBase,
    status_code=201,
    tags=["marcas-coche"],
    description="Crear una nueva marca de coche"
)
def create_marca_coche(marcaCoche_data: MarcaCocheBase):
    # Verificar si ya existe una marca de coche con el mismo nombre
    marca_existente = conn.execute(select(MarcaCocheBase).where(MarcaCocheBase.nombreMarca == marcaCoche_data.nombreMarca)).first()
    if marca_existente:
        raise HTTPException(status_code=400, detail="Ya existe una marca de coche con este nombre")

    nuevaMarcaCoche = {
        "nombreMarca": marcaCoche_data.nombreMarca
    }

    result = conn.execute(MarcaCocheBase.insert().values(nuevaMarcaCoche))
    nuevaMarcaCoche["id"] = result.lastrowid
    return nuevaMarcaCoche

@marcaCoche.put(
    "/marcas-coche/{id}",
    response_model=MarcaCocheBase,
    description="Modificar marca de coche por ID",
    tags=["marcas-coche"]
)
def update_marca_coche(marca_coche_data: MarcaCocheBase, id: int):
    # Verificar si la marca de coche con el ID proporcionado existe
    marca_coche_existente = conn.execute(select(MarcaCocheBase).where(MarcaCocheBase.c.id == id)).first()
    if marca_coche_existente is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")

    conn.execute(
        MarcaCocheBase.update()
        .values(
            nombreMarca=marca_coche_data.nombreMarca
        )
        .where(MarcaCocheBase.c.id == id)
    )

    return conn.execute(select(MarcaCocheBase).where(MarcaCocheBase.c.id == id)).first()

@marcaCoche.delete(
    "/marcas-coche/{id}",
    response_model=MarcaCocheBase,
    tags=["marcas-coche"],
    description="Eliminar una marca de coche por ID"
)
def delete_marca_coche(id: int):
    marcaEliminada = conn.execute(MarcaCocheBase.delete().where(MarcaCocheBase.c.id == id)).first()
    return marcaEliminada
