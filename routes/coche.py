from fastapi import APIRouter, HTTPException, Form  
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

@coche.post("/coches", tags=["coches"], response_model=CocheBase, description="Crear un nuevo coche")
async def create_coche(
    marca_id: int = Form(..., title="ID de la Marca", description="ID de la marca del coche"),
    modelo: str = Form(..., title="Modelo", description="Modelo del coche"),
    precio: float = Form(..., title="Precio", description="Precio del coche"),
    km: int = Form(..., title="Kilómetros", description="Kilómetros recorridos por el coche"),
    anio: int = Form(..., title="Año", description="Año de fabricación del coche"),
    cajaCambios: str = Form(..., title="Caja de Cambios", description="Tipo de caja de cambios del coche"),
    combustible: str = Form(..., title="Combustible", description="Tipo de combustible del coche"),
    distAmbiental: str = Form(..., title="Distancia Ambiental", description="Clasificación de la distancia ambiental del coche"),
    cilindrada: int = Form(..., title="Cilindrada", description="Cilindrada del coche"),
    tipCarr: str = Form(..., title="Tipo de Carrocería", description="Tipo de carrocería del coche"),
    color: str = Form(..., title="Color", description="Color del coche")
):
    marca_resultado = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == marca_id)).first()

    if marca_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")
    
    new_coche = {
        "marca_id": marca_id,
        "modelo": modelo,
        "precio": precio,
        "km": km,
        "anio": anio,
        "cajaCambios": cajaCambios,
        "combustible": combustible,
        "distAmbiental": distAmbiental,
        "cilindrada": cilindrada,
        "tipCarr": tipCarr,
        "color": color
    }

    result = conn.execute(Coche.insert().values(new_coche))
    new_coche["id"] = result.lastrowid
    return new_coche

@coche.put("/coches/{id}", tags=["coches"], response_model=CocheBase, description="Modificar coche por ID")
async def update_coche(
    id: int,
    marca_id: int = Form(..., title="ID de la Marca", description="ID de la marca del coche"),
    modelo: str = Form(..., title="Modelo", description="Modelo del coche"),
    precio: float = Form(..., title="Precio", description="Precio del coche"),
    km: int = Form(..., title="Kilómetros", description="Kilómetros recorridos por el coche"),
    anio: int = Form(..., title="Año", description="Año de fabricación del coche"),
    cajaCambios: str = Form(..., title="Caja de Cambios", description="Tipo de caja de cambios del coche"),
    combustible: str = Form(..., title="Combustible", description="Tipo de combustible del coche"),
    distAmbiental: str = Form(..., title="Distancia Ambiental", description="Clasificación de la distancia ambiental del coche"),
    cilindrada: int = Form(..., title="Cilindrada", description="Cilindrada del coche"),
    tipCarr: str = Form(..., title="Tipo de Carrocería", description="Tipo de carrocería del coche"),
    color: str = Form(..., title="Color", description="Color del coche")
):
    marca_resultado = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == marca_id)).first()
    
    if marca_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")

    conn.execute(
        Coche.update()
        .values(
            marca_id=marca_id,
            modelo=modelo,
            precio=precio,
            km=km,
            anio=anio,
            cajaCambios=cajaCambios,
            combustible=combustible,
            distAmbiental=distAmbiental,
            cilindrada=cilindrada,
            tipCarr=tipCarr,
            color=color
        )
        .where(Coche.c.id == id)
    )
    return conn.execute(select(Coche).where(Coche.c.id == id)).first()

@coche.delete("/coches/{id}", tags=["coches"], status_code=HTTP_204_NO_CONTENT)
def delete_coche(id: int):
    conn.execute(Coche.delete().where(Coche.c.id == id))
    return conn.execute(select(Coche).where(Coche.c.id == id)).first()