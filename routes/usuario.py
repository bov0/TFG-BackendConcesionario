from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from models.Usuario import Usuario
from schemas.Usuario import UsuarioBase
from config.db import conn
import io
from starlette.status import HTTP_204_NO_CONTENT

usuario = APIRouter()

@usuario.get(
    "/usuarios",
    tags=["usuarios"],
    response_model=list[UsuarioBase],
    description="Lista de todos los usuarios"
)
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
    
@usuario.get(
            "/usuarios/nombre/{nombre}",
            response_model=UsuarioBase,
            tags=["usuarios"],
            description="Ver usuario por nombre único")
def get_usuario(nombre : str):
    usuario = conn.execute(select(Usuario).where(Usuario.c.nombre == nombre)).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuario.get(
    "/usuarios/email/{email}",
    response_model=UsuarioBase,
    tags=["usuarios"],
    description="Ver usuario por email"
)
def get_usuario(email: str):
    usuario = conn.execute(select(Usuario).where(Usuario.c.Email == email)).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuario.post(
    "/usuarios",
    response_model=str,
    tags=["usuarios"],
    description="Crear un nuevo usuario")
async def create_usuario(
    nombre: str = Form(..., title="Nombre", description="Nombre del usuario"),
    apellidos: str = Form(..., title="Apellidos", description="Apellidos del usuario"),
    Email: str = Form(..., title="Email", description="Email del usuario"),
    contrasena: str = Form(...,title="Contrasena", description="Contrasena del usuario"),
    fotoPerfil: UploadFile = None  # Eliminar la restricción Form(...) para hacer que fotoPerfil sea opcional
):
    # Verificar si ya existe un usuario con el mismo email
    usuario_existente = conn.execute(select(Usuario).where(Usuario.c.id == id)).first()
    if usuario_existente is not None:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este email")

    foto_perfil_blob = None
    # Si se proporcionó una imagen, leer el archivo
    if fotoPerfil:
        foto_perfil_blob = await fotoPerfil.read()

    nuevoUsuario = {
        "nombre": nombre,
        "apellidos": apellidos,
        "Email": Email,
        "contrasena": contrasena,
        "fotoPerfil": foto_perfil_blob
    }

    result = conn.execute(Usuario.insert().values(nuevoUsuario))
    nuevoUsuario["id"] = result.lastrowid
    return f"Usuario {nombre} añadido"


@usuario.put("/usuarios/{id}",
             response_model=str,
            tags=["usuarios"],
             description="Modificar usuario por ID")
async def update_usuario(
    id: int,
    nombre: str = Form(..., title="Nombre", description="Nombre del usuario"),
    apellidos: str = Form(..., title="Apellidos", description="Apellidos del usuario"),
    Email: str = Form(..., title="Email", description="Email del usuario"),
    contrasena: str = Form(..., title="Contraseña", description="Contraseña del usuario"),
    fotoPerfil: UploadFile = None  # Eliminar la restricción Form(...) para hacer que fotoPerfil sea opcional
):

    # Verificar si el usuario con el ID proporcionado existe
    usuario_existente = conn.execute(select(Usuario).where(Usuario.c.id == id)).first()
    if usuario_existente is None:
        raise HTTPException(status_code=404, detail="No existe ningún usuario con el ID proporcionado")

    foto_perfil_blob = None
    # Si se proporcionó una imagen, leer el archivo
    if fotoPerfil:
        foto_perfil_blob = await fotoPerfil.read()
    
    UsuarioActualizado = conn.execute(Usuario.update().values(nombre=nombre,apellidos=apellidos,Email=Email,contrasena=contrasena,fotoPerfil=foto_perfil_blob).where(Usuario.c.id == id))
    
    if UsuarioActualizado is None:
        return f"error"

    return f"Usuario {nombre} actualizado"

@usuario.delete("/usuarios/{id}",
               tags=["usuarios"],
               description="Eliminar un usuario por ID")
def delete_usuario(id: int):
    delete_resultado = conn.execute(select(Usuario).where(Usuario.c.id == id)).first()
    
    if delete_resultado is None:
        raise HTTPException(status_code=404, detail="No existe ningún usuario con el ID proporcionado")
    
    conn.execute(Usuario.delete().where(Usuario.c.id == id))
    return "Usuario eliminado"

@usuario.get(
    "/imagen/{id}",
    response_model=UsuarioBase,
    tags=["usuarios"],
    description="Ver una imagen de usuario por ID del usuario"
)
async def ver_imagenUsuario(id: int):
    try:
        # Obtén la imagen de la base de datos por ID
        imagenUsuario = conn.execute(select(Usuario).where(Usuario.c.id == id)).first()

        if not imagenUsuario:
            raise HTTPException(status_code=404, detail="Imagen de usuario no encontrada")

        # Retorna la imagen como respuesta
        return StreamingResponse(io.BytesIO(imagenUsuario.fotoPerfil), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar la imagen: {str(e)}")
