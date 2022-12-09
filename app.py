from flask import Flask

from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('postgresql://username:userpass@db_pg:5432/testdb')

con = engine.connect()

nombre_tabla = engine.table_names()
print(nombre_tabla)

rs = con.execute("Select * from alias")
import pandas as pd
df = pd.DataFrame(rs.fetchall())
x = str(df.head())


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/')
def ping():
    return x 

@app.route('/login')
def login():
    return 'login'
    

if __name__=='__main__':
     
    app.run(host="0.0.0.0", port=5555, debug=True)