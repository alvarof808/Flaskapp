from flask import Flask, render_template, request, redirect, url_for, flash 

from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import Session
import psycopg2
from werkzeug.utils import secure_filename
import os

from marcado import marca

marca.leer()
app = Flask(__name__)
# Conexión a la base de datos
engine = create_engine('postgresql://username:userpass@db_pg:5432/testdb')

con = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
app.secret_key = 'mysecret_key'
Base = declarative_base()

app.config["UPLOAD_FOLDER"] =  "static/uploads/imgs"
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'docx']) 


# Funcion para limitar tipos de archivos que acepta el sistema
def permitidos_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

@app.route("/fotos")
def hello():
    return render_template('fotos.html')
# Ruta para cargar imagenes
@app.route("/add_img", methods=['POST'])
def add_img():
    if request.method == 'POST':
        file=request.files['foto']
        print(file)
        filename = secure_filename(file.filename)
        if permitidos_file(filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            pathI = "static/uploads/imgs/"+filename
            con.execute('INSERT INTO img (name, fecha, path) VALUES(%s, %s, %s)',('prueba', '01/03/2022', pathI))
            session.commit()
            flash('foto agregada') 
        #con.close()
        
    return redirect(url_for('hello'))
@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/add_doc', methods=['POST'])
def agregar_documento():
    if request.method == 'POST':
        fullname=request.form['fullname']
        apellido=request.form['apellido']
        cod_alias=request.form['cod_alias']
        con.execute('INSERT INTO alias (name, apellido, cod_alias) VALUES(%s, %s, %s)',
        (fullname, apellido, cod_alias))
        session.commit()
        flash('Alias agregado')
        #con.close()
    return redirect(url_for('index'))

@app.route('/marca_doc')
def seleccionar_documento():
    datos =con.execute('SELECT * FROM documento').fetchall()
    
    print(datos)
    return str(datos)
        
        


  

if __name__=='__main__':
     
    app.run(host="0.0.0.0", port=5555, debug=True)

