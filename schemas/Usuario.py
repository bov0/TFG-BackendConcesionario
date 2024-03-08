from pydantic import BaseModel
from typing import Union

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    Email: str
    fotoPerfil: bytes = None 