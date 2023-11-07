from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
#class User():
    def __init__(self, id, username , password, name='', apellido="" ) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.apellido = apellido
        
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
#Generar password de usuario de prueba
#print(generate_password_hash("alvaro"))

