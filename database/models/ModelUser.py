from database.models.entities.User import User
from connection.db import get_connection

class ModelUser():
    @classmethod
    def login(self, user):
        try:
            #cursor= db.connection.cursor()
            connection = get_connection()
            
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario, username, password, name, apellido FROM usuario WHERE username = '{}'".format(user.username))
                row= cursor.fetchone()
            
                if row != None:
                    user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4])
                    return user
                else:
                    return None
            connection.close()  
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, id):
        try:
            connection = get_connection()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario, username, name, apellido FROM usuario WHERE id_usuario = '{}'".format(id))
                row= cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
            connection.close()
        except Exception as ex:
            raise Exception(ex)