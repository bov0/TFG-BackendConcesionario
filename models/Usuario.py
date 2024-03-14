from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String, BLOB
from config.db import meta, engine

Usuario = Table('Usuario',
    meta,
    Column('id',Integer, primary_key=True),
    Column('nombre',String(255), nullable=False),
    Column('apellidos',String(255), nullable=False),
    Column('Email',String(255), nullable=False),
    Column('contrasena',String(255), nullable=False),
    Column('fotoPerfil',BLOB, nullable=True),
    )

meta.create_all(bind=engine,tables=[Usuario])