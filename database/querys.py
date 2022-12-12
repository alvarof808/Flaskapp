from connection.db import get_connection

def nombre_documento(id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM documento where id_documento = {0}'.format(id))
            datos = cursor.fetchall()
        connection.close()
        return datos[0][1]

    except Exception as ex:
        raise Exception(ex)
    
def fullname_alias(id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM alias where id_alias = {0}'.format(id))
            datos = cursor.fetchall()
        connection.close()
        return datos[0][1]
    except Exception as ex:
        raise Exception(ex)