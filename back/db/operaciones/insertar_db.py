from db.operaciones import conectarse_db, commitear

### - Hacer un wrapper para que cualquiera de estas funciones
###   no haga que se detenga el main si es que reciben una
###   excepción. Implementar un exception handler.
### - ¿Cómo guardamos las contraseñas?
### - ¿Qué tipo de dato usamos con las fechas? Definir para estandarizar.
### - ¿Debería crear un tipo de dato para solucionar el bad smell de
###   Long Parameter List?
### - ¿Debería hacer una validación previa para los datos antes
###   de enviarlos a la BD? <-- esto se hace en los services
### - ¿Cómo reacciono ante los errores de parte del motor de la BD? 
### - ¿Cómo devuelvo los errores de Foreign Keys?

## FUNCIONES QUE INSERTAN FILAS EN LAS TABLAS DE LA BD

def insertar_actividad(nombre: str, precio_mensual: float):
    """Permite insertar una fila para la tabla Actividad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Actividad (nombre, precio_mensual)
                                VALUES ('{nombre}', {precio_mensual});""")
    commitear(cursor)

def insertar_mensualidad(fecha_ini, fecha_fin, usuario_id: int):
    """Permite insertar una fila para la tabla Mensualidad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id)
                                VALUES ('{fecha_ini}', '{fecha_fin}', {usuario_id});""")
    commitear(cursor)

def insertar_permiso(nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)

def insertar_profesor(nombre: str, apellido: str, genero: str, dni: int):
    """Permite insertar una fila para la tabla Profesor"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}');""")
    commitear(cursor)

def insertar_rol(nombre: str):
    """Permite insertar una fila para la tabla Rol"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Rol (nombre) 
                                VALUES ('{nombre}');""")
    commitear(cursor)

def insertar_usuario(dni: int, nombre: str, apellido: str, edad: int, contraseña: str, correo: str, telefono: int, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario (dni, nombre, apellido, edad, contraseña, correo, telefono, genero)
                                VALUES({dni}, '{nombre}', '{apellido}', {edad}, '{contraseña}', '{correo}', '{telefono}', '{genero}');""")
    commitear(cursor)

def insertar_administrador(dni: int):
    """Permite insertar una fila para la tabla Administrador"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Administrador (dni)
                                VALUES ({dni});""")
    commitear(cursor)

def insertar_recepcionista(dni: int):
    """Permite insertar una fila para la tabla Recepcionista"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Recepcionista (dni)
                                VALUES ({dni});""")
    commitear(cursor)

def insertar_empleado(nombre: str, apellido: str, correo: str, contraseña: str, genero: str, dni: int, rol_id: int):
    """Permite insertar una fila para la tabla Empleado"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Empleado (nombre, apellido, correo, contraseña, genero, dni, rol_id)
                                VALUES ('{nombre}', '{apellido}', '{correo}', '{contraseña}', '{genero}', {dni}, {rol_id});""")
    commitear(cursor)

def insertar_rol_tener_permiso(rol_id: int, permiso_id: int):
    """Permite insertar una fila para la tabla Rol_Tener_Permiso"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Rol_Tener_Permiso (rol_id, permiso_id)
                                VALUES ({rol_id}, {permiso_id});""")
    commitear(cursor)

def insertar_sala(nombre: str):
    """Permite insertar una fila para la tabla Sala"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Sala (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)

def insertar_clase(estado: str, actividad_id: int, profesor_id: int):
    """Permite insertar una fila para la tabla Clase"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Clase (estado, actividad_id, profesor_id)
                                VALUES ('{estado}', {actividad_id}, {profesor_id});""")
    commitear(cursor)

def insertar_clase_ocurrir_sala(clase_id: int, sala_id: int, fecha: str):
    """Permite insertar una fila para la tabla Clase_Ocurrir_Sala"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Clase_Ocurrir_Sala (clase_id, sala_id, fecha)
                                VALUES ({clase_id}, {sala_id}, '{fecha}');""")
    commitear(cursor)

def insertar_descuento(nombre: str):
    """Permite insertar una fila para la tabla Descuento"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Descuento (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)

def insertar_usuario_tener_descuento(usuario_id: int, descuento_id: int):
    """Permite insertar una fila para la tabla Usuario_Tener_Descuento"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario_Tener_Descuento (usuario_id, descuento_id)
                                VALUES ({usuario_id}, {descuento_id});""")
    commitear(cursor)

def insertar_usuario_inscribir_clase(usuario_id: int, clase_id: int, fecha: str):
    """Permite insertar una fila para la tabla Usuario_Inscribir_Clase"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario_Inscribir_Clase (usuario_id, clase_id, fecha)
                                VALUES ({usuario_id}, {clase_id}, '{fecha}');""")
    commitear(cursor)

def insertar_usuario_cancelar_clase(usuario_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Usuario_Cancelar_Clase"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario_Cancelar_Clase (usuario_id, clase_id)
                                VALUES ({usuario_id}, {clase_id});""")
    commitear(cursor)

def insertar_pago(monto: float, usuario_id: int):
    """Permite insertar una fila para la tabla Pago"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Pago (monto, usuario_id)
                                VALUES ({monto}, {usuario_id});""")
    commitear(cursor)

def insertar_clase_tener_mensualidad(mensualidad_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Clase_Tener_Mensualidad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Clase_Tener_Mensualidad (mensualidad_id, clase_id)
                                VALUES ({mensualidad_id}, {clase_id});""")
    commitear(cursor)

def insertar_pago_pagar_clase(pago_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Pago_Pagar_Clase"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Pago_Pagar_Clase (pago_id, clase_id)
                                VALUES ({pago_id}, {clase_id});""")
    commitear(cursor)

def insertar_pago_pagar_mensualidad(pago_id: int, mensualidad_id: int):
    """Permite insertar una fila para la tabla Pago_Pagar_Mensualidad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Pago_Pagar_Mensualidad (pago_id, mensualidad_id)
                                VALUES ({pago_id}, {mensualidad_id});""")
    commitear(cursor)