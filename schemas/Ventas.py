from pydantic import BaseModel

class VentasBase(BaseModel):
    id: int
    coche_id: int
    comprador_id: int