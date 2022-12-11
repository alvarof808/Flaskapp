# Conexion a la base de datos
from config import config
from connection.db import get_connection

# Framework Flask
from flask import Flask, render_template, request, redirect, url_for, flash 

# Libreria para guardar Imágenes y documentos
from werkzeug.utils import secure_filename
import os
# Marcado de documento
from marcado import marca


app = Flask(__name__)



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
    try:
        if request.method == 'POST':
            connection = get_connection()
            file=request.files['foto']
            filename = secure_filename(file.filename)
            
            with connection.cursor() as cursor:
                if permitidos_file(filename):
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    pathI = "static/uploads/imgs/"+filename
                    cursor.execute('INSERT INTO img (name, fecha, path) VALUES(%s, %s, %s)',
                               ('prueba', '01/03/2022', pathI))
                    add_img = cursor.rowcount
                    connection.commit()
                    flash('foto agregada') 
            connection.close()
        return redirect(url_for('hello'))  
            
    except Exception as ex:
        raise Exception(ex)
        


@app.route('/')
def index ():
    return render_template('index.html')

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
        return render_template('alias_select.html', files = datos, doc =name)
    except Exception as ex:
        raise Exception(ex)

@app.route('/marcar_documento', methods=['POST'])
def marcar_documento():
    
    pass
    

        
# Funcion captura error 404 Paginas no encotradas
def pagina_no_encotrada(error):
    return "<h1>Página no encontrada</h1>", 404
  

if __name__=='__main__':
    app.config.from_object(config['development'])
    
    # Error Páginas no encontradas
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(host="0.0.0.0", port=5555)


#, debug=True