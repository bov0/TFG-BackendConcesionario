from pydantic import BaseModel
from typing import Union
from fastapi import UploadFile

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    Email: str
    fotoPerfil: bytes = None 