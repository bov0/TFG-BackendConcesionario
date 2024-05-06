from pydantic import BaseModel

class VentaBase(BaseModel):
    id: int
    coche_id: int
    comprador_id: int