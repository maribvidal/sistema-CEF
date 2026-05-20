from db.operaciones.commitear_db import commitear
from db.operaciones.conectar_db import conectarse_db

def ejecutar_fetchall(query):

    try:
        cursor = conectarse_db()

        cursor.execute(query)

        resultado = cursor.fetchall()

        # me tiraba error por el tipo de dato que devuelve el fetchall, así que lo convertí a una lista de diccionarios
        datos = [dict(fila) for fila in resultado]

        cursor.connection.close()

        return {
            "status": "success",
            "data": datos
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def ejecutar_fetchone(query):

    try:
        cursor = conectarse_db()

        cursor.execute(query)

        resultado = cursor.fetchone()

        cursor.connection.close()

        return {
            "status": "success",
            "data": resultado
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
def ejecutar_insertar(query):

    try:
        cursor = conectarse_db()

        cursor.execute(query)
        
        nuevo_id = cursor.lastrowid

        commitear(cursor)

        return {
            "status": "success",
            "data": nuevo_id
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def ejecutar_query(query):

    try:
        cursor = conectarse_db()

        cursor.execute(query)

        commitear(cursor)

        return {
            "status": "success",
            "data": None
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

## Wrapper que realiza una acción y commitea, además de
## manejar excepciones

def manejar_db(func):
    def wrapper(*args, **kwargs):
        try:
            cursor = conectarse_db()
            resultado = func(cursor, *args, **kwargs)

            commitear(cursor)
            print(" > Operación realizada con éxito")
            return resultado

        except Exception as e:
            print(f" > Error al realizar la operación: {str(e)}")
            cursor.connection.close()

    return wrapper
