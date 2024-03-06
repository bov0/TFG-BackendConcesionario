from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    Email: str
    fotoPerfil: bytes