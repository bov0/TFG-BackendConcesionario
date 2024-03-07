from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from models import Usuario
from schemas.Usuario import UsuarioBase
from config.db import conn

usuario = APIRouter()

@usuario.get(
        "/usuarios",
         tags=["usuarios"],
         response_model=list[UsuarioBase],
         description="Lista de todos los usuarios")
def get_usuarios():
    return conn.execute(select(Usuario)).fetchall()

@usuario.get(
            "/usuarios/{id}",
            response_model=UsuarioBase,
            tags=["usuarios"],
            description="Ver usuario por ID único")
def get_usuario(id : int):
    usuario = conn.execute(select(UsuarioBase).where(UsuarioBase.id == id)).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuario.post(
        "/",
        response_model=UsuarioBase,
        status_code=201,
        tags=["usuarios"],
        description="Crear un nuevo usuario")
def create_usuario(usuario_data: UsuarioBase):
    # Verificar si ya existe un usuario con el mismo email
    usuarioExistente = conn.execute(select(UsuarioBase).where(UsuarioBase.email == usuario_data.email)).first()
    if usuarioExistente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este email")

    nuevoUsuario = {
        "nombre": usuario_data.nombre,
        "apellidos": usuario_data.apellidos,
        "email": usuario_data.email,
        "fotoPerfil": usuario_data.fotoPerfil
    }

    result = conn.execute(UsuarioBase.insert().values(nuevoUsuario))
    nuevoUsuario["id"] = result.lastrowid
    return nuevoUsuario

@usuario.put("/usuarios/{id}", response_model=UsuarioBase, description="Modificar usuario por ID")
def update_usuario(usuario_data: UsuarioBase, id: int):

    # Verificar si el usuario con el ID proporcionado existe
    usuario_existente = conn.execute(select(UsuarioBase).where(UsuarioBase.id == id)).first()
    if usuario_existente is None:
        raise HTTPException(status_code=404, detail="No existe ningún usuario con el ID proporcionado")

    conn.execute(
        UsuarioBase.update()
        .values(
            nombre=usuario_data.nombre,
            apellidos=usuario_data.apellidos,
            email=usuario_data.email,
            fotoPerfil=usuario_data.fotoPerfil
        )
        .where(UsuarioBase.c.id == id)
    )

    return conn.execute(select(UsuarioBase).where(UsuarioBase.c.id == id)).first()

@usuario.delete("/usuarios/{id}",
               response_model=UsuarioBase,
               tags=["usuarios"],
               description="Eliminar un usuario por ID")
def delete_usuario(id: int):
    usuarioEliminado = conn.execute(UsuarioBase.delete().where(UsuarioBase.id == id)).first()
    return usuarioEliminado