import sqlite3 as sqlite

def ejecutar_fetchall(query, cursor):
    """Ejecuta una consulta SQL que devuelve varias filas y 
        maneja las excepciones."""
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()

        # me tiraba error por el tipo de dato que devuelve el fetchall, así que lo convertí a una lista de diccionarios
        datos = [dict(fila) for fila in resultado]

        return {
            "status": "success",
            "data": datos
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def ejecutar_fetchone(query, cursor) -> dict:
    try:
        print("Ejecutando query de consulta: ", query)
        cursor.execute(query)
        
        resultado = cursor.fetchone()
        resultado = dict(resultado) if resultado else None

        print("Resultado consulta: ", resultado)
        return {
            "status": "success",
            "data": resultado
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
def ejecutar_insertar(query, cursor):
    """Ejecuta una consulta SQL de inserción y maneja 
        las excepciones."""
    try:
        print("Ejecutando query de inserción: ", query)
        cursor.execute(query)
        print("Query ejecutada exitosamente.")
        nuevo_id = cursor.lastrowid
        print("ID del nuevo registro insertado: ", nuevo_id)

        cursor.connection.commit()
        print("Cambios commiteados exitosamente.")

        return {
            "status": "success",
            "data": nuevo_id
        }

    except Exception as e:
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
        print("ERROR SQL:")
        print(e)

        return {
            "status": "error",
            "message": str(e)
        }
