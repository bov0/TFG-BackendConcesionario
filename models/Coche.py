from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine

Coche = Table(
    'coches',
    meta,
    Column('id',Integer, primary_key=True),
    Column('marca_id',Integer, ForeignKey('marcaCoche.id'), nullable=False),
    Column('modelo',String(255), nullable=False),
    Column('precio',Float, nullable=False),
    Column('km',Integer, nullable=False),
    Column('anio',Integer, nullable=False),
    Column('cajaCambios',String(50), nullable=False),
    Column('combustible',String(50), nullable=False),
    Column('distAmbiental',String(50), nullable=False),
    Column('cilindrada',Integer, nullable=False),
    Column('tipCarr',String(50), nullable=False),
    Column('color',String(50), nullable=False),
    )

meta.create_all(bind=engine,tables=[Coche])