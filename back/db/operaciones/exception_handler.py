import sqlite3 as sqlite

def ejecutar_fetchall(query, cursor):
    """Ejecuta una consulta SQL que devuelve varias filas y 
        maneja las excepciones."""
    fallo = True
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        # me tiraba error por el tipo de dato que devuelve el fetchall, así que lo convertí a una lista de diccionarios
        datos = [dict(fila) for fila in resultado]
        if resultado is None or str(resultado) == '[]':
            fallo = False
            raise ValueError("Algo falló en la consulta (el resultado es None).")

        return {
            "status": "success",
            "data": datos
        }

    except Exception as e:
        if (fallo):
            print(f" >> Error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

def ejecutar_fetchone(query, cursor) -> dict:
    fallo = True
    try:
        cursor.execute(query)
        resultado = cursor.fetchone()
        if resultado is None:
            fallo = False
            raise ValueError("Algo falló en la consulta (el resultado es None).")

        resultado = dict(resultado)

        return {
            "status": "success",
            "data": resultado
        }

    except Exception as e:
        if (fallo):
            print(f" >> Error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
        
def ejecutar_insertar(query, cursor):
    """Ejecuta una consulta SQL de inserción y maneja 
        las excepciones."""
    fallo = True
    try:
        cursor.execute(query)
        nuevo_id = cursor.lastrowid
        if nuevo_id is None:
            fallo = False
            raise ValueError("No se pudo insertar el registro.")

        cursor.connection.commit()

        return {
            "status": "success",
            "data": nuevo_id
        }

    except Exception as e:
        if (fallo):
            print(f" >> Error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

def ejecutar_query(query, cursor):
    """Ejecuta una consulta SQL que no devuelve datos 
        y maneja las excepciones."""
    try:
        cursor.execute(query)
        cursor.connection.commit()
        return {
            "status": "success",
            "data": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
