from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

MarcaCoche = Table(
    'MarcaCoche',
    meta,
    Column('id',Integer, primary_key=True),
    Column('nombreMarca',String(255), nullable=False)
    )

meta.create_all(bind=engine,tables=[MarcaCoche])
