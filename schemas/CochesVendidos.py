from pydantic import BaseModel

class CocheVendidoBase(BaseModel):
    id: int
    marca_id: int
    modelo: int
    precio: float
    km: int
    anio: int
    cajaCambios: str
    combustible: str
    distAmbiental: str
    cilindrada: int
    tipCarr: str
    color: str
    vendedor_id: int