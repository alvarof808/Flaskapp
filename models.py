from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Date, Integer, String, ForeignKey

engine = create_engine('postgresql://username:userpass@db_pg:5432/testdb')


meta = MetaData(engine)

usuario = Table(
    'usuario', meta,
    Column('id_usuario', Integer, primary_key = True, autoincrement=True),
    Column('name', String),
    Column('apellido', String),
    Column('username', String),
    Column('pass', String)
)

alias = Table(
    'alias', meta,
    Column('id_alias', Integer, primary_key = True, autoincrement=True),
    Column('name', String),
    Column('apellido', String),
    Column('cod_alias', String)
)

documento = Table(
    'documento', meta,
    Column('id_documento', Integer, primary_key = True, autoincrement=True),
    Column('name', String),
    Column('path', String),
    Column('fecha', Date)    
)

documento_Marca = Table(
    'documento_Marca', meta,
    Column('id_documento_Marca', Integer, primary_key = True, autoincrement=True),
    Column('id_documento', None, ForeignKey('documento.id_documento')),
    Column('nuevo_name', String),
    Column('fecha', Date)    
)

img = Table(
    'img', meta,
    Column('id_img', Integer, primary_key = True, autoincrement=True),
    Column('name', String),
    Column('path', String),
    Column('fecha', Date)
)

resultado = Table(
    'resultado', meta,
    Column('id_resultado', Integer, primary_key = True, autoincrement=True),
    Column('id_img', None, ForeignKey('img.id_img')),
    Column('alias', String),
    Column('fecha', Date)
    
)

marca = Table(
    'marca', meta,
    Column('id_marca', Integer, primary_key = True, autoincrement=True),
    Column('id_documento', None, ForeignKey('documento.id_documento')),
    Column('id_alias', None, ForeignKey('alias.id_alias')),
    Column('nuevo_doc', String),
    Column('palabra', String)
)

meta.create_all()