from pydantic import BaseModel

class ModeloCocheBase(BaseModel):
    id: int
    nombre: str
    marca_id: int