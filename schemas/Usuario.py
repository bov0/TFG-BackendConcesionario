from pydantic import BaseModel
from fastapi import UploadFile

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    Email: str
    fotoPerfil: UploadFile