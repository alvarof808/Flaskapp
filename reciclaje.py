#from markupsafe import escape
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import Session
#import psycopg2

# Conexión a la base de datos
""" engine = create_engine('postgresql://username:userpass@db_pg:5432/testdb')

con = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
app.secret_key = 'mysecret_key'
Base = declarative_base() """

""" @app.route("/add_img", methods=['POST'])
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
        
    return redirect(url_for('hello')) """
"""     
    datos =con.execute('SELECT * FROM documento').fetchall()
    
    print(datos)  """
    
"""for x in l:
    for n in x:
                            txt = open(n,"r")
                            lista  = txt.read()
                            txt.close()
                            lista = lista[0:-1]
                            lista = lista[1:]
                            lista = lista.split("]") """
                            
import pickle

with open("/app/static/txt/prueba1_Estefany.pickle", "rb") as f:
    obj = pickle.load(f) 
    
print(obj)
        