from pydantic import BaseModel
from enum import Enum

class CajaCambiosEnum(Enum):
    Manual = "Manual"
    Automatico = "Automatico"

class CombustibleEnum(Enum):
    Gasolina = "Gasolina"
    Diesel = "Diesel"
    Hibrido = "Hibrido"
    Electrico = "Electrico"
    GLP = "GLP"

class DistAmbientalEnum(Enum):
    Cero = "Cero"
    Eco = "Eco"
    C = "C"
    B = "B"

class TipoCarrEnum(Enum):
    Sedan = "Sedan"
    Coupe = "Coupe"
    SUV = "SUV"
    Camioneta = "Camioneta"

class ColorEnum(Enum):
    Rojo = "Rojo"
    Azul = "Azul"
    Amarillo = "Amarillo"
    Negro = "Negro"
    Blanco = "Blanco"

class CocheBase(BaseModel):
    marca_id: int
    modelo: str
    precio: float
    km: int
    anio: int
    cajaCambios: CajaCambiosEnum
    combustible: CombustibleEnum
    distAmbiental: DistAmbientalEnum
    cilindrada: int
    tipCarr: TipoCarrEnum
    color: ColorEnum
