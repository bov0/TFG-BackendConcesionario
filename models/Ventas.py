from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from config.db import meta, engine

Ventas = Table(
    'Ventas',
    meta,
    Column('id',Integer, primary_key=True),
    Column('coche_id',Integer, ForeignKey('cochesVendidos.id'), nullable=False),
    Column('comprador_id',Integer,ForeignKey('Usuario.id'),nullable=False),
)

meta.create_all(bind=engine,tables=[Ventas])