from fastapi import APIRouter, HTTPException, Form  
from config.db import conn
from models.Coche import Coche, CajaCambiosEnum,CombustibleEnum,ColorEnum,DistAmbientalEnum, TipoCarrEnum
from models.MarcaCoche import MarcaCoche
from models.ModeloCoche import ModeloCoche
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
async def get_coches():
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
    modelo: str = Form(..., title="Modelo", description="ID del modelo del coche"),
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
    marcaExiste = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == marca_id)).first()

    if marcaExiste is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")
    
    modeloExiste = conn.execute(select(ModeloCoche).where(ModeloCoche.c.id == int(modelo))).first()

    if modeloExiste is None:
        raise HTTPException(status_code=404, detail="No existe ningun modelo de coche con el ID proporcionado")
    
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

from fastapi import HTTPException

@coche.put("/coches/{id}", tags=["coches"], response_model=dict, description="Modificar coche por ID")
async def update_coche(
    id: int,
    marca_id: int = Form(None, title="ID de la Marca", description="ID de la marca del coche"),
    modelo: str = Form(None, title="Modelo", description="Modelo del coche"),
    precio: float = Form(None, title="Precio", description="Precio del coche"),
    km: int = Form(None, title="Kilómetros", description="Kilómetros recorridos por el coche"),
    anio: int = Form(None, title="Año", description="Año de fabricación del coche"),
    cajaCambios: str = Form(None, title="Caja de Cambios", description="Tipo de caja de cambios del coche"),
    combustible: str = Form(None, title="Combustible", description="Tipo de combustible del coche"),
    distAmbiental: str = Form(None, title="Distancia Ambiental", description="Clasificación de la distancia ambiental del coche"),
    cilindrada: int = Form(None, title="Cilindrada", description="Cilindrada del coche"),
    tipCarr: str = Form(None, title="Tipo de Carrocería", description="Tipo de carrocería del coche"),
    color: str = Form(None, title="Color", description="Color del coche")
):
    # Verificar si el coche con el ID proporcionado existe
    coche_existente = conn.execute(select(Coche).where(Coche.c.id == id)).first()
    if coche_existente is None:
        raise HTTPException(status_code=404, detail=f"No existe ningún coche con el ID {id}")

    # Construir el diccionario de valores de actualización
    camposActualizados = {k: v for k, v in locals().items() if v is not None and k not in ['id', 'coche_existente', 'conn']}

    # Verificar si hay algún campo para actualizar
    if not camposActualizados:
        raise HTTPException(status_code=422, detail="No se proporcionaron campos para actualizar")

    conn.execute(
        Coche.update()
        .values(camposActualizados)
        .where(Coche.c.id == id)
    )

    # Devolver el coche actualizado como un diccionario
    return conn.execute(select(Coche).where(Coche.c.id == id)).first()._asdict()

@coche.delete("/coches/{id}", tags=["coches"], status_code=HTTP_204_NO_CONTENT)
def delete_coche(id: int):
    conn.execute(Coche.delete().where(Coche.c.id == id))
    return conn.execute(select(Coche).where(Coche.c.id == id)).first()

@coche.get("/opcionesCajaCambios", tags=["enums"], response_model=List[str], description="Obtener opciones de caja de cambios")
def get_opciones_caja_cambios():
    return [caja.value for caja in CajaCambiosEnum]

@coche.get("/opcionesCombustible", tags=["enums"], response_model=List[str], description="Obtener opciones de combustible")
def get_opciones_combustible():
    return [combustible.value for combustible in CombustibleEnum]

@coche.get("/opcionesDistAmbiental", tags=["enums"], response_model=List[str], description="Obtener opciones de distancia ambiental")
def get_opciones_dist_ambiental():
    return [dist_ambiental.value for dist_ambiental in DistAmbientalEnum]

@coche.get("/opcionesTipoCarr", tags=["enums"], response_model=List[str], description="Obtener opciones de tipo de carrocería")
def get_opciones_tipo_carr():
    return [tipo_carr.value for tipo_carr in TipoCarrEnum]

@coche.get("/opcionesColor", tags=["enums"], response_model=List[str], description="Obtener opciones de color")
def get_opciones_color():
    return [color.value for color in ColorEnum]