from fastapi import APIRouter, HTTPException, UploadFile, Form
from sqlalchemy import select
from models.Usuario import Usuario
from schemas.Usuario import UsuarioBase
from config.db import conn
from starlette.status import HTTP_204_NO_CONTENT

from werkzeug.utils import secure_filename

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
    usuario = conn.execute(select(Usuario).where(Usuario.c.id == id)).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuario.post(
    "/usuarios",
    response_model=UsuarioBase,
    status_code=201,
    tags=["usuarios"],
    description="Crear un nuevo usuario")
def create_usuario(
    nombre: str = Form(..., title="Nombre", description="Nombre del usuario"),
    apellidos: str = Form(..., title="Apellidos", description="Apellidos del usuario"),
    Email: str = Form(..., title="Email", description="Email del usuario"),
    fotoPerfil: UploadFile = Form(..., title="Foto", description="Foto del usuario")
):
    # Verificar si ya existe un usuario con el mismo email
    usuario_existente = conn.execute(select(Usuario).where(Usuario.c.email == email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este email")
    
    # Verificar si se proporcionó un archivo
    #if not fotoPerfil.filename:
        #raise HTTPException(status_code=422, detail="No se proporcionó una imagen")

    foto_perfil_blob = fotoPerfil.read()

    nuevoUsuario = {
        "nombre": nombre,
        "apellidos": apellidos,
        "Email": Email,
        "fotoPerfil": foto_perfil_blob
    }

    result = conn.execute(UsuarioBase.insert().values(nuevoUsuario))
    nuevoUsuario["id"] = result.lastrowid
    return nuevoUsuario


@usuario.put("/usuarios/{id}",
             response_model=UsuarioBase,
            tags=["usuarios"],
             description="Modificar usuario por ID")
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
               tags=["usuarios"],
               status_code=HTTP_204_NO_CONTENT,
               description="Eliminar un usuario por ID")
def delete_usuario(id: int):
    delete_resultado = conn.execute(select(Usuario).where(Usuario.c.id == id)).first()
    
    if delete_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ningun ususario con el ID proporcionado")
    
    usuarioEliminado = conn.execute(Usuario.delete().where(Usuario.c.id == id)).first()
    return {"mensaje": "Marca eliminada"}