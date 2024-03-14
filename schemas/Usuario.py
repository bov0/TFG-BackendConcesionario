from pydantic import BaseModel
from typing import Optional
import base64

class UsuarioBase(BaseModel):
    id : int
    nombre: str
    apellidos: str
    Email: str
    contrasena: str
    fotoPerfil: Optional[bytes] = None

    class Config:
        # Define un método personalizado para convertir el campo fotoPerfil a una cadena de bytes
        json_encoders = {
            bytes: lambda v: base64.b64encode(v).decode() if v is not None else None
        }
