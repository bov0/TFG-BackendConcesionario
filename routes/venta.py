from fastapi import APIRouter, HTTPException, Form
from sqlalchemy import select
from models.Venta import Venta
from schemas.Venta import VentaBase
from config.db import conn
from starlette.status import HTTP_204_NO_CONTENT

venta = APIRouter()

@venta.get(
    "/ventas",
    tags=["ventas"],
    response_model=list[VentaBase],
    description="Lista de todas las ventas"
)
async def get_ventas():
    return conn.execute(select(Venta)).fetchall()

@venta.get(
    "/ventas/{id}",
    tags=["ventas"],
    response_model=VentaBase,
    description="Venta por Id único"
)
async def get_venta(id: int):
    venta_coche = conn.execute(select(Venta).where(Venta.c.id == id)).first()
    if venta_coche is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta_coche

@venta.post(
    "/ventas",
    response_model=VentaBase,
    status_code=201,
    tags=["ventas"],
    description="Crear una nueva venta"
)
async def create_venta(
    coche_id: int = Form(..., tittle="CocheID", description="Id del coche"),
    comprador_id: int = Form(..., tittle="CompradorID", description="Id del comprador")
):
    # Verificar si ya existe una marca de coche con el mismo nombre
    venta_existente = conn.execute(select(Venta).where(Venta.c.coche_id == coche_id)).first()

    if venta_existente:
        raise HTTPException(status_code=400, detail="Ya existe una venta para ese coche")

    nuevaVenta = {
        "coche_id": coche_id,
        "comprador_id": comprador_id
    }

    result = conn.execute(Venta.insert().values(nuevaVenta))
    nuevaVenta["id"] = result.lastrowid
    return nuevaVenta

@venta.put(
    "/ventas/{id}",
    response_model=VentaBase,
    status_code=201,
    tags=["ventas"],
    description="Modificar una venta"
)
async def update_venta(
    id: int,
    coche_id: int = Form(..., tittle="CocheID", description="Id del coche"),
    comprador_id: int = Form(..., tittle="CompradorID", description="Id del comprador")
):
    # Verificar si la marca de coche con el ID proporcionado existe
    venta_existente = conn.execute(select(Venta).where(Venta.c.id == id)).first()

    if venta_existente is None:
        raise HTTPException(status_code=404, detail="No existe ninguna marca de coche con el ID proporcionado")

    conn.execute(
        Venta.update()
        .values(
            coche_id=coche_id,
            comprador_id=comprador_id
        )
        .where(Venta.c.id == id)
    )

    return conn.execute(select(Venta).where(Venta.c.id == id)).first()

@venta.delete(
    "/ventas/{id}",
    status_code=HTTP_204_NO_CONTENT,
    tags=["ventas"],
    description="Eliminar una venta"
)
async def delete_marca_coche(id: int):
    ventaEliminada = conn.execute(Venta.delete().where(Venta.c.id == id))
    return {"mensaje": "Venta eliminada"}