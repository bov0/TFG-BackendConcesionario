from pydantic import BaseModel

class CocheBase(BaseModel):
    marca_id: int
    modelo: str
    precio: float
    km: int
    anio: int
    cajaCambios: str
    combustible: str
    distAmbiental: str
    cilindrada: int
    tipCarr: str
    color: str