# Conexion a la base de datos
from config import config
from connection.db import get_connection
from database import querys
# Framework Flask
from flask import Flask, render_template, request, redirect, url_for, flash 
# Libreria para fechas
from datetime import datetime

# Libreria para guardar Imágenes y documentos
from werkzeug.utils import secure_filename
import os
# Marcado de documento
from marcado import marca, direcciones


app = Flask(__name__)



app.config["UPLOAD_FOLDER"] =  "static/uploads/imgs"
app.config["UPLOAD_DOCX"] = "static/uploads/documentos"
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

# Ruta del template carga de imagenes
@app.route("/carga_img")
def carga_img():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM documento')
            datos = cursor.fetchall()
        connection.close()
        return render_template('carga_img.html', files = datos)
    except Exception as ex:
        raise Exception(ex)
    
# Ruta para cargar imagenes


@app.route("/add_img", methods=['POST'])
def add_img():
    try:
        if request.method == 'POST':
            connection = get_connection()
            file=request.files['foto']
            id_doc=request.form['doc']
            filename = secure_filename(file.filename)
            fil = filename.split('.')
            
            with connection.cursor() as cursor:
                if permitidos_file(filename):
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    pathI = "static/uploads/imgs/"+filename
                    cursor.execute('INSERT INTO img (name, fecha, path) VALUES(%s, %s, %s)',
                               (fil[0], datetime.now(), pathI))
                    
                    add_img = cursor.rowcount
                    connection.commit()
                    cursor.execute('SELECT palabra FROM marca WHERE id_documento={0}'.format(id_doc))
                    txts = cursor.fetchall()
                    
                    #flash('foto agregada') 
            connection.close()
        return txts
        #return redirect(url_for('hello'))  
            
    except Exception as ex:
        raise Exception(ex)
        


@app.route('/')
def index ():
    return render_template('index.html')


# Funcion para insertar valores en tabla Alias
@app.route('/add_doc', methods=['POST'])
def agregar_documento():
    try:
        if request.method == 'POST':
            connection = get_connection()
            with connection.cursor() as cursor:
                # Captura todos los datos obtenidos del form 
                fullname=request.form['fullname']
                apellido=request.form['apellido']
                cod_alias=request.form['cod_alias']
                # Insertar los datos obtenidos en tabla
                cursor.execute('INSERT INTO alias (name, apellido, cod_alias) VALUES(%s, %s, %s)',
                (fullname, apellido, cod_alias))
                connection.commit()
                flash('Alias agregado')
            connection.close()
        return redirect(url_for('index'))
    except Exception as ex:
        raise Exception(ex)
# Funcion para obtener el listado de documentos y mostrarlo en listado.html via /lista_doc
@app.route('/lista_doc')
def seleccionar_documento():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM documento')
            datos = cursor.fetchall()
        connection.close()
        
        return render_template('lista_doc.html', files = datos)
    except Exception as ex:
        raise Exception(ex)
    
@app.route('/select_alias/<string:name>')
def seleccionar_alias(name):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM alias')
            datos = cursor.fetchall()
        connection.close()
        nombre = querys.nombre_documento(name)
        return render_template('alias_select.html', files = datos, doc =nombre, id = name)
    except Exception as ex:
        raise Exception(ex)

@app.route('/marcar_documento', methods=['POST'])
def marcar_documento():
    try:
        if request.method == 'POST':
            connection = get_connection()
            with connection.cursor() as cursor:
                alias = request.form['alias']
                id_doc = request.form['id_doc']
                name_alias = querys.fullname_alias(alias)
                doc = querys.nombre_documento(id_doc)
                valores = marca.marcado_docx(name_alias,doc)
                
                cursor.execute('INSERT INTO marca (id_documento, id_alias, posicion, palabra) VALUES(%s, %s, %s, %s)',(id_doc, alias, 0, direcciones.path_txt(valores)))
                connection.commit()
               
            connection.close()   
        return valores
    except Exception as ex:
        raise Exception(ex)
    
# Funcion para Agregar documentos en list_doc
@app.route("/doc_add", methods=['POST'])   
def add_doc():
    try:
        if request.method == 'POST':
            connection = get_connection()
            file=request.files['doc']
            
            filename = secure_filename(file.filename)
            fil = filename.split('.')
            
            with connection.cursor() as cursor:
                if permitidos_file(filename):
                    file.save(os.path.join(app.config["UPLOAD_DOCX"], filename))
                    pathI = "static/uploads/documentos/"+filename
                    cursor.execute('INSERT INTO documento (name, path, fecha) VALUES(%s, %s, %s)',
                               (fil[0] , pathI, datetime.now()))
                    
                    add_img = cursor.rowcount
                    connection.commit()
                    
                    flash('documento agregada') 
            connection.close()
        
        return redirect(url_for('seleccionar_documento'))
    except Exception as ex:
        raise Exception(ex)



        
# Funcion captura error 404 Paginas no encotradas
def pagina_no_encotrada(error):
    return "<h1>Página no encontrada</h1>", 404
  

if __name__=='__main__':
    app.config.from_object(config['development'])
    
    # Error Páginas no encontradas
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(host="0.0.0.0", port=5555)


#, debug=True