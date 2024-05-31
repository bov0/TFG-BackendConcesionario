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

@ventas.get("/compras/{id_comprador}", tags=["compras"], response_model=List[VentasBase], description="Ver venta por ID único")
async def get_venta(id_comprador: int):
    coches_resultado = conn.execute(select(Ventas).where(Ventas.c.comprador_id == id_comprador)).fetchall()
    
    if coches_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ninguna ventas con el ID proporcionado")
    
    return coches_resultado
    
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

@ventas.get("/ventasComprador/{comprador_id}", tags=["ventas"], response_model=VentasBase, description="Ver ventas por ID del comprador")
async def get_venta(comprador_id: int):
    coche_resultado = conn.execute(select(Ventas).where(Ventas.c.comprador_id == comprador_id)).fetchall()
    
    if coche_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ninguna ventas con el ID proporcionado")
    
    return coche_resultado

@ventas.delete("/ventas/{id}", tags=["ventas"], status_code=HTTP_204_NO_CONTENT)
async def delete_venta(id: int):
    conn.execute(Ventas.delete().where(Ventas.c.id == id))
    return conn.execute(select(Ventas).where(Ventas.c.id == id)).first()