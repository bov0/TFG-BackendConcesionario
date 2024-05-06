from ast import For
from fastapi import APIRouter, HTTPException, Form  
from config.db import conn
from models.Ventas import Ventas
from schemas.Ventas import VentasBase
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import select

ventas = APIRouter()

@ventas.get(
    "/ventas",
    tags=["ventas"],
    response_model=List[VentasBase],
    description="Lista de todas las ventas",
)
async def get_coches():
    return conn.execute(select(Ventas)).fetchall()

@ventas.get("/ventas/{id}", tags=["ventas"], response_model=VentasBase, description="Ver venta por ID único")
async def get_coche(id: int):
    coche_resultado = conn.execute(select(Ventas).where(Ventas.c.id == id)).first()
    
    if coche_resultado is None:
        raise HTTPException(status_code=404, detail="No se encontró ninguna ventas con el ID proporcionado")
    
    return coche_resultado  

@ventas.post("/ventas", tags=["ventas"], response_model=VentasBase, description="Crear un nuevo coche")
async def create_coche(
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
def delete_coche(id: int):
    conn.execute(Ventas.delete().where(Ventas.c.id == id))
    return conn.execute(select(Ventas).where(Ventas.c.id == id)).first()