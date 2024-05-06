from pydantic import BaseModel
from models.Coche import CajaCambiosEnum,CombustibleEnum,DistAmbientalEnum,TipoCarrEnum,ColorEnum

class CocheBase(BaseModel):
    id: int
    marca_id: int
    modelo: int
    precio: float
    km: int
    anio: int
    cajaCambios: CajaCambiosEnum
    combustible: CombustibleEnum
    distAmbiental: DistAmbientalEnum
    cilindrada: int
    tipCarr: TipoCarrEnum
    color: ColorEnum
    vendedor_id: int