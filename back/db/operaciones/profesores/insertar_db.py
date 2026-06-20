from db.operaciones.exception_handler import ejecutar_insertar

def insertar_profesor(nombre: str, 
                      apellido: str, 
                      telefono: str, 
                      genero: str, 
                      dni: int, 
                      actividades: list,
                      cursor):
    """Permite insertar una fila para la tabla Profesor"""
    query_usuario = f"""INSERT INTO Usuario (nombre, apellido, telefono, genero, dni, rol_id)
                VALUES('{nombre}', '{apellido}', '{telefono}', '{genero}', '{dni}', 5);"""

    resultado = ejecutar_insertar(query_usuario, cursor)

    if resultado['status'] == 'success':
        # Entonces sacamos el id real solo para armar el SQL    
        id_real = resultado['data']

        for actividad_id in actividades:
            query_actividad = f"""INSERT INTO Profesor_Actividad (profesor_id, actividad_id)
                                            VALUES({id_real}, {actividad_id});"""
            cursor.execute(query_actividad)
    
    # Entonces devolvemos el diccionario para no romper nada con el resto de la app
    return resultado
