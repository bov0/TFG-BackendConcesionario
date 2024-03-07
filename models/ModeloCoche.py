from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta,engine

ModeloCoche = Table(
    'ModeloCoche',
    meta,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(255), nullable=False),
    Column('marca_id', Integer, ForeignKey('MarcaCoche.id'), nullable=False)
)

meta.create_all(bind=engine,tables=[ModeloCoche])
