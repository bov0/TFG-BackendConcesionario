from sqlalchemy import create_engine, MetaData

MYSQLDB_HOST = "db4free.net"
MYSQLDB_USUARIO = "ivan_fdez02"
MYSQLDB_PASSWORD = "palomeras"
MYSQLDB_BD = "iesdawivan02"

#Conexión a Google Cloud SQL
#MYSQLDB_HOST = "34.175.31.241"
#MYSQLDB_USUARIO = "admin"
#MYSQLDB_PASSWORD = "admin1234"
#MYSQLDB_BD = "iesdawivan02"

db_url = f"mysql+pymysql://{MYSQLDB_USUARIO}:{MYSQLDB_PASSWORD}@{MYSQLDB_HOST}/{MYSQLDB_BD}"

engine = create_engine(db_url)

meta = MetaData()

conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")