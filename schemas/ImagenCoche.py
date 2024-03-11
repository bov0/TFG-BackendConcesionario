from pydantic import BaseModel
import base64

class ImagenCocheBase(BaseModel):
    coche_id: int
    imagen: bytes = None


    class Config:
        json_encoders = {
            bytes: lambda v: base64.b64encode(v).decode() if v is not None else None
        }
