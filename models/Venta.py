from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer
from config.db import meta, engine

Venta = Table(
    'Ventas',
    meta,
    Column('id',Integer, primary_key=True),
    Column('coche_id',Integer, nullable=False),
    Column('comprador_id',Integer, nullable=False)
    )

meta.create_all(bind=engine,tables=[Venta])