from fastapi import APIRouter, HTTPException, Form  
from config.db import conn
from models.Ventas import Ventas
from models.Coche import Coche
from schemas.Ventas import VentasBase
from schemas.Coche import CocheBase
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import select,join

ventas = APIRouter()

@ventas.get(
    "/ventas",
    tags=["ventas"],
    response_model=List[VentasBase],
    description="Lista de todas las ventas",
)
async def get_ventas():
    return conn.execute(select(Ventas)).fetchall()

@ventas.get("/ventas/{id}", tags=["ventas"], response_model=VentasBase, description="Ver venta por ID único")
async def get_venta(id: int):
    coche_resultado = conn.execute(select(Ventas).where(Ventas.c.id == id)).first()
    
    if coche_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ninguna ventas con el ID proporcionado")
    
    return coche_resultado

@ventas.get(
    "/coches-comprados/{comprador_id}",
    tags=["ventas"],
    response_model=List[CocheBase],
    description="Obtener todos los coches comprados por un comprador basado en su ID",
)
async def obtener_coches_comprados(comprador_id: int):
    try:
        # Realiza el join entre Ventas y Coche para obtener coches comprados
        join_ventas_coches = join(Ventas, Coche, Ventas.coche_id == Coche.id)

        coche_resultado = conn.execute(select(Coche).where(Coche.c.id == comprador_id)).fetchall()
        
        return coche_resultado

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener los coches comprados: {str(e)}",
        )
    
@ventas.post("/ventas", tags=["ventas"], response_model=VentasBase, description="Crear una venta")
async def create_venta(
    coche_id: int = Form(..., title="ID de la Marca", description="ID de la marca del coche"),
    comprador_id: int = Form(..., title="ID del comprador", description="ID del comprador"),
):
    
    new_venta = {
        "coche_id": coche_id,
        "comprador_id": comprador_id
    }

    result = conn.execute(Ventas.insert().values(new_venta))
    new_venta["id"] = result.lastrowid
    return new_venta

from fastapi import HTTPException

@ventas.delete("/ventas/{id}", tags=["ventas"], status_code=HTTP_204_NO_CONTENT)
def delete_venta(id: int):
    conn.execute(Ventas.delete().where(Ventas.c.id == id))
    return conn.execute(select(Ventas).where(Ventas.c.id == id)).first()