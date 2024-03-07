from pydantic import BaseModel
from fastapi import UploadFile

class ImagenCocheBase(BaseModel):
    coche_id: int
    imagen: UploadFile