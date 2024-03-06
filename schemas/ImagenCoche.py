from pydantic import BaseModel

class ImagenCocheBase(BaseModel):
    coche_id: int
    imagen: bytes