# Conexion a la base de datos
from config import config
from connection.db import get_connection
from database import querys


from database.models.ModelUser import ModelUser
from database.models.entities.User import User
# Framework Flask
from flask import Flask, render_template, request, redirect, url_for, flash 

from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager, login_user, logout_user, login_required
# Libreria para fechas
from datetime import datetime

from analisis import lectura

# Libreria para guardar Imágenes y documentos
from werkzeug.utils import secure_filename
import os
# Marcado de documento
from marcado import marca, direcciones
# Lectura de img

#from lectura1 import lectura

import pickle


app = Flask(__name__)
csrf = CSRFProtect()

login_manager_app = LoginManager(app)


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

def obtener_path_doc(id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT palabra FROM marca WHERE id_documento={0}'.format(id))
        txts = cursor.fetchall()
        connection.close()  
        datos = txts
     
    return datos
   
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
                    connection.commit()
                    add_img = cursor.rowcount
                    l = obtener_path_doc(id_doc)
                    lista = []
                    n = []
                    for i in l:
                        with open(str(i[0]), "rb") as f:
                            alias1 = i[0]
                            alias = alias1[16:-7]
                            obj = pickle.load(f)
                            lista.append(alias)
                            n.append(lectura.lectura_img(pathI,obj, alias)) 
                    #open(file)
                    #flash('foto agregada')
            connection.close()
            t = list(n)
            teff = None
            for i in t:
                if i != "desconocido":
                    teff = i
                
            #x = marca.getEliminarRepetidos(n)
            
        
        #return redirect(url_for('hello'), n) 
        return  redirect(f'/resultado/{teff}') 
            
    except Exception as ex:
        raise Exception(ex)
        
# Funcion para mostrar resultado
@app.route('/resultado/<name>')
@login_required
def mostrar_resultado(name):
    #name = name[2:-2]
    if name != None:
        connection = get_connection()
        with connection.cursor() as cursor:
            #cursor.execute("SELECT a.name, a.apellido  from alias a, marca b where a.id_alias = b.id_alias and b.nuevo_doc ='{0}'".format(direcciones.path_pdf(name)))
            cursor.execute("SELECT a.name, a.apellido  from alias a, marca b where a.id_alias = b.id_alias and b.nuevo_doc = '{0}';".format(direcciones.path_pdf(name)))
            t = cursor.fetchall()
        connection.close()
        name = name+".pdf"
        otro = "sfasdfasd"
    else :
        # Aqui se encontro a los desconocidos 11-12-2022
        name = "Desconocido"
        t = None
        otro = "Desconocido"
    #t = "desconocido"
    #name.remove("Desconocido")
    return render_template("resultado.html", p = t, d = name)
    #return t

@app.route('/')
def index():
    return redirect(url_for('login'))


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

# Route que envia al home de la app
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =="POST":
        
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña invalida...")
                return render_template('login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('login.html')
    else:
        return render_template('login.html')

# Funcion Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('index.html')


@app.route('/list_alias')
@login_required
def lista_alias():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM alias')
            datos = cursor.fetchall()
        connection.close()
        
        return render_template('list_alias.html', files = datos)
    except Exception as ex:
        raise Exception(ex)
    
    

#Funcion para agregar alias
@app.route('/add_alias', methods=['POST'])
def agregar_alias():
    try:
        if request.method == 'POST':
            connection = get_connection()
            with connection.cursor() as cursor:
                # Captura todos los datos obtenidos del form 
                fullname=request.form['fullname']
                apellido=request.form['apellido']
                
                cod_alias=fullname[0:3].lower()+"_"+apellido[0:3].lower()
                # Insertar los datos obtenidos en tabla
                cursor.execute('INSERT INTO alias (name, apellido, cod_alias) VALUES(%s, %s, %s)',
                (fullname, apellido, cod_alias))
                connection.commit()
                flash('Alias agregado')
            connection.close()
        return redirect(url_for('lista_alias'))
    except Exception as ex:
        raise Exception(ex)
    
    pass


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
                
                cod_alias=fullname[0:3].lower()+"_"+apellido[0:3].lower()
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
@login_required
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
    
    
# Funcion para seleccionar el alias con el que se desea marcar el documento   
@app.route('/select_alias/<string:name>')
@login_required
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
                
                cursor.execute('INSERT INTO marca (id_documento, id_alias, nuevo_doc, palabra) VALUES(%s, %s, %s, %s)',(id_doc, alias,direcciones.path_pdf(valores), direcciones.path_txt(valores)))
                connection.commit()
                
            connection.close()   
        return  redirect(f'/descarga_pdf/{valores}')
    except Exception as ex:
        raise Exception(ex)
    
# Funcion para descargar Documento PDF
@app.route("/descarga_pdf/<string:name>")
@login_required
def descarga_pdf(name):
    x = direcciones.path_pdf(name)
    return render_template("descargar_pdf.html", pdf = x)
    
    


    
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

#Route login
#@app.route('/login')
#def login():
#     return render_template("login.html")

def status_401(error):
    return redirect(url_for('login'))
        
# Funcion captura error 404 Paginas no encotradas
def pagina_no_encotrada(error):
    return render_template("404.html"), 404
  

if __name__=='__main__':
    app.config.from_object(config['development'])
    #csrf.init_app(app)
    # Error Páginas no encontradas
    app.register_error_handler(404, pagina_no_encotrada)
    app.register_error_handler(401, status_401)
    app.run(host="0.0.0.0", port=5555)


#, debug=True