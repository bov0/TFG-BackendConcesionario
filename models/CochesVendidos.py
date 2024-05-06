from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float
from config.db import meta, engine

CochesVendidos = Table(
    'cochesVendidos',
    meta,
    Column('id', Integer, primary_key=True),
    Column('marca_id', Integer, ForeignKey('MarcaCoche.id'), nullable=False),
    Column('modelo', Integer, ForeignKey('ModeloCoche.id'), nullable=False),
    Column('precio', Float, nullable=False),
    Column('km', Integer, nullable=False),
    Column('anio', Integer, nullable=False),
    Column('cajaCambios', String(255), nullable=False),
    Column('combustible', String(255), nullable=False),
    Column('distAmbiental', String(255), nullable=False),
    Column('cilindrada', Integer, nullable=False),
    Column('tipCarr', String(255), nullable=False),
    Column('color', String(255), nullable=False),
    Column('vendedor_id',Integer,ForeignKey('Usuario.id'), nullable=False)
)

meta.create_all(bind=engine, tables=[CochesVendidos])