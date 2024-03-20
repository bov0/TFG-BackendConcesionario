from pydantic import BaseModel

class MarcaCocheBase(BaseModel):
    id: int
    nombreMarca: str
