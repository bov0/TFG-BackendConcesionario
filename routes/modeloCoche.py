from fastapi import APIRouter, HTTPException , Form 
from config.db import conn
from models.ModeloCoche import ModeloCoche
from models.MarcaCoche import MarcaCoche
from schemas.ModeloCoche import ModeloCocheBase
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import select

modeloCoche = APIRouter()

@modeloCoche.get(
    "/modelos",
    tags=["modelos"],
    response_model=List[ModeloCocheBase],
    description="Lista de todos los modelos",
)
def get_all():
    return conn.execute(select(ModeloCoche)).fetchall()

@modeloCoche.get(
    "/modelosMarca/{id}",
    tags=["modelos"],
    response_model=List[ModeloCocheBase],
    description="Lista de todos los modelos por marca de coche",
)
def get_modeloByMarca(id: int):
    modelo_resultado = conn.execute(select(ModeloCoche).where(ModeloCoche.c.marca_id == id)).fetchall()

    if modelo_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ningún modello con el ID de la marca proporcionado")
    
    return modelo_resultado

@modeloCoche.get(
    "/modelos/{id}",
    tags=["modelos"],
    response_model=ModeloCocheBase,
    description="Lista de todos los modelos por Id único",
)
def get_modeloById(id: int):
    modelo_resultado = conn.execute(select(ModeloCoche).where(ModeloCoche.c.id == id)).first()

    if modelo_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ningún modello con el ID del modelo proporcionado")
    
    return modelo_resultado

@modeloCoche.post(
    "/modelos",
    tags=["modelos"],
    response_model=ModeloCocheBase,
    description="Crear un nuevo modelo",
)
async def create_modelo(
    nombre: str = Form(..., tittle="Nombre", description="Nombre del modelo"),
    marca_id: int = Form(..., title="ID de la Marca", description="ID de la marca del coche")
):
    marca_resultado = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == marca_id)).first()

    if marca_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")
    
    new_modelo = {
        "nombre": nombre,
        "marca_id": marca_id
    }

    result = conn.execute(ModeloCoche.insert().values(new_modelo))
    new_modelo["id"] = result.lastrowid
    return new_modelo

@modeloCoche.put(
    "/modelos/{id}",
    tags=["modelos"],
    response_model=ModeloCocheBase,
    description="Modifica un modelo dado un Id",
)
async def update_modelo(
    id: int,
    nombre: str = Form(..., tittle="Nombre", description="Nombre del modelo"),
    marca_id: int = Form(..., title="ID de la Marca", description="ID de la marca del coche")
):
    marca_resultado = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == marca_id)).first()
    
    if marca_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")
    conn.execute(
        ModeloCoche.update().values(nombre=nombre, marca_id=marca_id).where(ModeloCoche.c.id == id)
    )
    modelo_actualizado = conn.execute(select(ModeloCoche).where(ModeloCoche.c.id == id)).first()
    if modelo_actualizado is None:
        raise HTTPException(status_code=404, detail="No existe ningún modelo con el ID proporcionado")
    
    return modelo_actualizado

@modeloCoche.delete(
    "/modelos/{id}",
    tags=["modelos"],
    status_code=HTTP_204_NO_CONTENT,
    description="Elimina un modelo dado un Id",
)
def delete_modelo(id:int):
    conn.execute(ModeloCoche.delete().where(ModeloCoche.c.id == id))
    return "Modelo eliminado"
