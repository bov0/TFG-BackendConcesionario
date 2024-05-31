from fastapi import APIRouter, HTTPException, Form  
from config.db import conn
from models.CochesVendidos import CochesVendidos
from models.MarcaCoche import MarcaCoche
from models.ModeloCoche import ModeloCoche
from schemas.CochesVendidos import CocheVendidoBase
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import null, select

cocheVendido = APIRouter()

@cocheVendido.get(
    "/cochesVendidos",
    tags=["cochesVendidos"],
    response_model=List[CocheVendidoBase],
    description="Lista de todos los coches",
)
async def get_coches():
    return conn.execute(select(CochesVendidos)).fetchall()

@cocheVendido.get("/cochesVendidos/{id}", tags=["cochesVendidos"], response_model=CocheVendidoBase, description="Ver coche por ID único")
async def get_coche(id: int):
    coche_resultado = conn.execute(select(CochesVendidos).where(CochesVendidos.c.id == id)).first()
    
    if coche_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ningún coche con el ID proporcionado")
    
    return coche_resultado

@cocheVendido.post("/cochesVendidos", tags=["cochesVendidos"], response_model=CocheVendidoBase, description="Crear un nuevo coche")
async def create_coche(
    id: int = Form(..., title="ID del coche Vendido", description="ID del coche Vendido"),
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
    color: str = Form(..., title="Color", description="Color del coche"),
    vendedor_id: int = Form(...,title="Vendedor", description="ID del vendedor")
):
    marcaExiste = conn.execute(select(MarcaCoche).where(MarcaCoche.c.id == marca_id)).first()

    if marcaExiste is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")
    
    modeloExiste = conn.execute(select(ModeloCoche).where(ModeloCoche.c.id == int(modelo))).first()

    if modeloExiste is None:
        raise HTTPException(status_code=404, detail="No existe ningun modelo de coche con el ID proporcionado")
    
    new_coche = {
        "id": id,
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
        "color": color,
        "vendedor_id" : vendedor_id
    }

    result = conn.execute(CochesVendidos.insert().values(new_coche))
    new_coche["id"] = result.lastrowid
    return new_coche

from fastapi import HTTPException

@cocheVendido.delete("/cochesVendidos/{id}", tags=["cochesVendidos"], status_code=HTTP_204_NO_CONTENT)
async def delete_coche(id: int):
    conn.execute(CochesVendidos.delete().where(CochesVendidos.c.id == id))
    return conn.execute(select(CochesVendidos).where(CochesVendidos.c.id == id)).first()

@cocheVendido.get(
    "/coches-vendidos/{vendedor_id}",
    tags=["cochesVendidos"],
    response_model=List[CocheVendidoBase],
    description="Obtener todos los coches vendidos por un vendedor basado en su ID",
)
async def obtener_coches_comprados(vendedor_id: int):
    try:

        coche_resultado = conn.execute(select(CochesVendidos).where(CochesVendidos.c.vendedor_id == vendedor_id)).fetchall()
        
        if coche_resultado is None:
            raise HTTPException(status_code=404, detail="No existe ningun coche vendido por el usuario con id " + vendedor_id)

        return coche_resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener los coches comprados: {str(e)}",
        )