from fastapi import APIRouter, HTTPException  
from config.db import conn
from models.Coche import Coche
from models.MarcaCoche import MarcaCoche
from schemas.Coche import CocheBase
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import select

coche = APIRouter()

@coche.get(
    "/coches",
    tags=["coches"],
    response_model=List[CocheBase],
    description="Lista de todos los coches",
)
def get_coches():
    return conn.execute(select(Coche)).fetchall()

@coche.get("/coches/{id}", tags=["coches"], response_model=CocheBase, description="Ver coche por ID único")
def get_coche(id: int):
    coche_resultado = conn.execute(select(Coche).where(Coche.c.id == id)).first()
    
    if coche_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ningún coche con el ID proporcionado")
    
    return coche_resultado

@coche.post("/", tags=["coches"], response_model=CocheBase, description="Crear un nuevo coche")
async def create_coche(coche_data: CocheBase):

    marca_resultado = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == coche_data.marca_id)).first()

    if marca_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")
    
    new_coche = {
        "marca_id": coche_data.marca_id,
        "modelo": coche_data.modelo,
        "precio": coche_data.precio,
        "km": coche_data.km,
        "anio": coche_data.anio,
        "cajaCambios": coche_data.cajaCambios,
        "combustible": coche_data.combustible,
        "distAmbiental": coche_data.distAmbiental,
        "cilindrada": coche_data.cilindrada,
        "tipCarr": coche_data.tipCarr,
        "color": coche_data.color
    }

    result = conn.execute(Coche.insert().values(new_coche))
    new_coche["id"] = result.lastrowid
    return new_coche

@coche.put(
    "/coches/{id}", tags=["coches"], response_model=CocheBase, description="Modificar coche por ID"
)
def update_coche(coche_data: CocheBase, id: int):

    marca_resultado = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == coche_data.marca_id)).first()
    
    if marca_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")

    conn.execute(
        Coche.update()
        .values(
            marca_id=coche_data.marca_id,
            modelo=coche_data.modelo,
            precio=coche_data.precio,
            km=coche_data.km,
            anio=coche_data.anio,
            cajaCambios=coche_data.cajaCambios,
            combustible=coche_data.combustible,
            distAmbiental=coche_data.distAmbiental,
            cilindrada=coche_data.cilindrada,
            tipCarr=coche_data.tipCarr,
            color=coche_data.color
        )
        .where(Coche.c.id == id)
    )
    return conn.execute(select(Coche).where(Coche.c.id == id)).first()

@coche.delete("/{id}", tags=["coches"], status_code=HTTP_204_NO_CONTENT)
def delete_coche(id: int):
    conn.execute(Coche.delete().where(Coche.c.id == id))
    return conn.execute(select(Coche).where(Coche.c.id == id)).first()