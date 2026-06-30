from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_query
from db.operaciones.reservas.borrar_db import eliminar_reservas_usuario

# falta implementar & testear
def modificar_empleado(
        cursor,
        empleado_dni: int,
        dni_nuevo = None,
        nombre = None, 
        apellido = None, 
        correo = None, 
        genero = None, 
        rol_id = None,
        actividades = None
    ) -> dict:
    """Modifica un empleado específico en la base de datos, utilizando su ID como referencia.
        Recibe el ID del empleado a modificar y los nuevos datos (nombre, apellido, cargo, salario).
        Devuelve un diccionario con el resultado de la operación."""

    query_verificacion = f"""
        SELECT id, nombre, apellido, correo, genero, rol_id
        FROM Usuario
        WHERE dni = {empleado_dni}
    """
    usuario = ejecutar_fetchone(query_verificacion, cursor)

    if not usuario or usuario["data"] is None:
        return {
            "status": "error",
            "message": "Empleado no encontrado"
        }
    # Ahora se agrega el profesor en el rango...
    elif usuario["data"]["rol_id"] not in (0, 1, 2, 5): 
        return {
            "status": "error",
            "message": "El usuario no es un empleado"
        }

    datos_actuales = usuario["data"]
    usuario_id = datos_actuales["id"] # Necesitamos capturar el ID real

    dni_final = empleado_dni if (dni_nuevo is None) else dni_nuevo
    nombre_final = nombre if nombre is not None else datos_actuales["nombre"]
    apellido_final = apellido if apellido is not None else datos_actuales["apellido"]
    genero_final = genero if genero is not None else datos_actuales["genero"]
    rol_id_final = rol_id if rol_id is not None else datos_actuales["rol_id"]
    
    # CONTROL AD-HOC: Si no es un profesor y su correo es el mismo, se va a recibir en
    # el modificar_empleado_service.

    query_update = f"""
        UPDATE Usuario
        SET dni = {dni_final},
            nombre = '{nombre_final}',
            apellido = '{apellido_final}',"""
    if correo is not None:
<<<<<<< HEAD
        query_update += f"correo = '{correo}',"   
=======
        query_update += f"correo = '{correo}',"
>>>>>>> 0406601b8ff7e7ecb23471ac74d50fcb7b03fcea
    query_update += f"""genero = '{genero_final}',
            rol_id = {rol_id_final}
        WHERE dni = {empleado_dni}
    """

    res_update = ejecutar_query(query_update, cursor)

    if res_update["status"] == "success" and rol_id_final == 5 and actividades:
        try:
            # Primero borramos todas las actividades viejas que tenia el profe
            cursor.execute(f"DELETE FROM Profesor_Actividad WHERE profesor_id = {usuario_id}")

            # E insertamos las nuevas
            for act_id in actividades:
                cursor.execute(f"INSERT INTO Profesor_Actividad (profesor_id, actividad_id) VALUES ({usuario_id}, {act_id})")
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al actualizar actividades del profesor: {str(e)}"
            }

    return res_update



def modificar_empleado_con_dni(
        empleado_dni: int,
        nuevo_dni: int,
        nombre: str, 
        apellido,
        correo,
        genero,
        rol_id, 
        cursor
    ) -> dict:
    """Hace lo mismo que la función de arriba, pero además permite
        modificar el dni mismo del empleado."""
    
    query_update = f"""
        UPDATE Usuario
        SET dni = {nuevo_dni},
            nombre = '{nombre}',
            apellido = '{apellido}',
            correo = '{correo}',
            genero = '{genero}',
            rol_id = {rol_id}
        WHERE dni = {empleado_dni}
    """

    print(query_update)

    return ejecutar_query(query_update, cursor)

def borrar_empleado(empleado_dni: int, cursor) -> dict:
    """Borra un empleado específico de la base de datos, utilizando su DNI como referencia.
        Recibe el DNI del empleado a borrar.
        Devuelve un diccionario con el resultado de la operación."""

    query_verificacion = f"SELECT id, rol_id FROM Usuario WHERE dni = {empleado_dni}"

    usuario = ejecutar_fetchone(query_verificacion, cursor)
    print("IMPRIMIENDO RESPUESTA DEL FETCHONEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",usuario)

    if usuario.get("status") == "error" or not usuario.get("data"):
        return { "status": "error", "message": "Empleado no encontrado" }

    rol_actual = usuario["data"]["rol_id"]

    # validar si ya es un usuario eliminardo (rol >= 20)
    if rol_actual >= 20:  
        return {
            "status": "error",
            "message": "El empleado ya estaba eliminado"
        }
    # Lógica del profesor
    elif rol_actual == 5: # o sea si el usuario es un profesor
        print("El usuario es un profesor, se procede a verificar si tiene clases a su cargo")
        profesor_id = usuario["data"]["id"]
        query_clases_profesor = f"""
            SELECT COUNT(*) as total_clases
            FROM Clase
            WHERE profesor_id = {profesor_id}
              AND estado != 'Borrado'
        """
        resultado_clases = ejecutar_fetchone(query_clases_profesor, cursor)
        print("RESULTADO DE LA CONSULTA DE CLASES DEL PROFESOR: ", resultado_clases)

        if resultado_clases.get("status") == "success" and resultado_clases["data"]["total_clases"] > 0:
            return {
                "status": "clases_asignadas",
                "message": f"No se puede eliminar al profesor. Tiene {resultado_clases['data']['total_clases']} clase/s asignada/s"
            }
    elif rol_actual == 3:
        print("hola?")
        resultado_limpieza = eliminar_reservas_usuario(usuario["data"]["id"], cursor)
        if resultado_limpieza.get("status") == "error":
            return {
                "status": "error",
                "message": "Error al intentar limpiar las reservas del usuario."
            }

    # Tras una consulta del profesor y charla con el equipo, se decidió que todos los empleados (incluido también clientes) sean de borrado lógico
    # si es un +20, es borrado lógico, 
    rol_actual += 20

    query_update = f"""
        UPDATE Usuario
        SET rol_id = {rol_actual}
        WHERE dni = {empleado_dni}
    """
    return ejecutar_query(query_update, cursor)

def desactivar_empleado(usuario_dni: int, cursor) -> dict:
    """Desactiva un empleado específico de la base de datos, utilizando su DNI como referencia.
        Recibe el DNI del empleado a desactivar.
        Devuelve un diccionario con el resultado de la operación."""

    query_verificacion = f"""
        SELECT rol_id
        FROM Usuario
        WHERE dni = {usuario_dni}
    """
    usuario = ejecutar_fetchone(query_verificacion, cursor)

    if not usuario:
        return {
            "status": "error",
            "message": "Usuario no encontrado"
        }
    
    rol_actual = usuario["data"]["rol_id"]
    if 10 <= rol_actual < 20:
        return {
            "status": "error",
            "message": "El empleado ya estaba desactivado"
        }
    if rol_actual >= 20:
        return {"status": "error", "message": "No se puede desactivar un usuario eliminado"}
    
    # Aplicamos la desactivación
    nuevo_rol = rol_actual + 10
    query_update = f"UPDATE Usuario SET rol_id = {nuevo_rol} WHERE dni = {usuario_dni}"

    return ejecutar_query(query_update, cursor)
