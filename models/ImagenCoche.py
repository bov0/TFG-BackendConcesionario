from sqlalchemy import Column, Table, ForeignKey, false
from sqlalchemy.sql.sqltypes import Integer, BLOB
from config.db import meta, engine

ImagenCoche = Table(
    'ImagenCoche',
    meta,
    Column('id',Integer, primary_key=True),
    Column('coche_id',Integer, ForeignKey('coches.id'), nullable=False),
    Column('imagen',BLOB,nullable=False)
)

meta.create_all(bind=engine,tables=[ImagenCoche])