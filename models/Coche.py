from sqlalchemy import Column, Table, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine
from enum import Enum as PythonEnum

class CajaCambiosEnum(PythonEnum):
    Manual = "Manual"
    Automatico = "Automatico"

class CombustibleEnum(PythonEnum):
    Gasolina = "Gasolina"
    Diesel = "Diesel"
    Hibrido = "Hibrido"
    Electrico = "Electrico"
    GLP = "GLP"

class DistAmbientalEnum(PythonEnum):
    Cero = "Cero"
    Eco = "Eco"
    C = "C"
    B = "B"

class TipoCarrEnum(PythonEnum):
    Sedan = "Sedan"
    Coupe = "Coupe"
    SUV = "SUV"
    Camioneta = "Camioneta"

class ColorEnum(PythonEnum):
    Rojo = "Rojo"
    Azul = "Azul"
    Amarillo = "Amarillo"
    Negro = "Negro"
    Blanco = "Blanco"

Coche = Table(
    'coches',
    meta,
    Column('id', Integer, primary_key=True),
    Column('marca_id', Integer, ForeignKey('MarcaCoche.id'), nullable=False),
    Column('modelo', Integer, ForeignKey('ModeloCoche.id'), nullable=False),
    Column('precio', Float, nullable=False),
    Column('km', Integer, nullable=False),
    Column('anio', Integer, nullable=False),
    Column('cajaCambios', Enum(CajaCambiosEnum), nullable=False),
    Column('combustible', Enum(CombustibleEnum), nullable=False),
    Column('distAmbiental', Enum(DistAmbientalEnum), nullable=False),
    Column('cilindrada', Integer, nullable=False),
    Column('tipCarr', Enum(TipoCarrEnum), nullable=False),
    Column('color', Enum(ColorEnum), nullable=False),
)

meta.create_all(bind=engine, tables=[Coche])