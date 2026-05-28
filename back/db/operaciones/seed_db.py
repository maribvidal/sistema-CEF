from db.operaciones.mensualidades.insertar_db import insertar_mensualidad
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.permisos.insertar_db import insertar_permiso
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones.clase_ocurrir_sala.insertar_db import insertar_clase_ocurrir_sala
from db.operaciones import insertar_pago, insertar_clase
from db.operaciones import insertar_pago_pagar_clase, insertar_usuario_inscribir_clase_por_id

# necesito insertarle mensualidades con actividades a los usuarios
def insertar_datos(cursor):  
    # Crear usuarios
    insertar_usuario(12345678, 'Juan', 'Pérez', '123333333', '2004-10-10', 'juan.perez@example.com', "1234",'M', 1, cursor)
    insertar_usuario(87654321, 'María', 'Gómez', '45644444', '2008-07-10', 'maria.gomez@example.com', "5678",'F', 3, cursor)
    insertar_usuario(39674828, 'Ernesto', 'Garcia', '12345678', '1997-07-10', 'ernesto.garcia@example.com', "5678",'M', 2, cursor)
    insertar_usuario(32031512, 'Lourdes', 'Gonzales', '6543713241', '1992-07-05', 'lourdes.gonzales@example.com', "5678",'F', 2, cursor)
    insertar_usuario(34673342, 'Gaspar', 'Solari', '7325466314', '2008-07-10', 'gaspar.solari@example.com', "5678",'M', 1, cursor)
   
    # Crear solo usuarios comunes

    # Crear profesores
    id_prof1 = insertar_profesor('Carlos', 'López', 'M', 11223344, cursor)
    insertar_profesor('Ana', 'Martínez', 'F', 44332211, cursor)

    id_prof1 = id_prof1['data']

    # Crear actividades
    insertar_actividad('Yoga', 50.0, cursor)
    insertar_actividad('Pilates', 60.0, cursor)
    insertar_actividad('Funcional', 70.0, cursor)

    insertar_mensualidad('2026-01-01', '2026-12-01', 1, cursor)
    insertar_mensualidad('2026-02-02', '2026-12-02', 2, cursor)

    # Crear permisos
    insertar_permiso('Metricas', cursor)

    # Crear roles
    insertar_rol('Administrador', cursor)
    insertar_rol('Recepcionista', cursor)
    
    # Crear salas
    insertar_sala('Sala 1', 10, cursor)
    insertar_sala('Sala 2', 25, cursor)
    insertar_sala('Sala 3', 20, cursor)

    # Crear clase
    id_clas = insertar_clase('Programada', 1, id_prof1, 5, cursor)
    id_clas = id_clas['data']
    res_clase_ocu_sala = insertar_clase_ocurrir_sala(id_clas, 1, '2024-07-01', '10:00', cursor)
    
    # Inscribir usuario a clase
    id_clase_ocu_sala = res_clase_ocu_sala['data']
    insertar_usuario_inscribir_clase_por_id(1, id_clas, id_clase_ocu_sala, cursor)

    # Crear pagos
    insertar_pago(50.0, 1, cursor)
    insertar_pago(60.0, 2, cursor)

    # Crear pagos pagar clase
    insertar_pago_pagar_clase(1, 1, cursor)

    generar_mas_datos_db_operaciones(cursor)

def generar_mas_datos_db_operaciones(cursor):
    try:
        # 1. Crear 30 usuarios comunes (rol_id = 3)
        ids_usuarios_creados = []
        print("Insertando 30 usuarios comunes...")
        
        for i in range(1, 31):
            res_usuario = insertar_usuario(
                dni=10000000 + i,
                nombre=f"Socio{i}",
                apellido="Prueba",
                contraseña="pass12345",
                fecha_nac="1995-01-01",
                correo=f"socio{i}@gym.com",
                telefono=f"22100000{i:02d}",
                genero="M" if i % 2 == 0 else "F",
                rol=3,
                cursor=cursor
            )
            
            # Guardamos el ID autogenerado para usarlo en la inscripción
            if res_usuario['status'] == 'success':
                ids_usuarios_creados.append(res_usuario['data'])
            else:
                print(f"Fallo al insertar usuario {i}: {res_usuario['message']}")

        # 2. Insertar la clase con 25 cupos
        # Asumimos que la actividad con id=1 y el profesor con id=1 ya existen en la DB
        print("Insertando la clase...")
        res_clase = insertar_clase(
            estado="Publicada",
            actividad_id=1,
            profesor_id=1,
            cupo_maximo=25,
            cursor=cursor
        )

        if res_clase['status'] == 'success':
            clase_id = res_clase['data']
            
            # 3. Insertar la relación Clase_Ocurrir_Sala
            # Asumimos que la sala con id=1 ya existe en la DB
            print("Asignando sala y horario a la clase...")
            res_ocurrencia = insertar_clase_ocurrir_sala(
                clase_id,  # respuesta2['data'] en tu código
                1,         # sala_id
                "2026-06-01", # fecha
                "18:00",      # hora
                cursor
            )

            if res_ocurrencia['status'] == 'success':
                id_clase_ocu_sala = res_ocurrencia['data']
                
                # 4. Inscribir a los primeros 20 usuarios en la clase
                print("Inscribiendo 20 usuarios en la clase...")
                usuarios_a_inscribir = ids_usuarios_creados[:20]
                
                for id_usuario in usuarios_a_inscribir:
                    res_inscripcion = insertar_usuario_inscribir_clase_por_id(
                        id_usuario,
                        clase_id,
                        id_clase_ocu_sala,
                        cursor
                    )
                    
                    if res_inscripcion['status'] != 'success':
                        print(f"Error al inscribir usuario {id_usuario}: {res_inscripcion['message']}")
                        
                print("Las 20 inscripciones se insertaron correctamente.")
            else:
                print(f"Error al asignar sala: {res_ocurrencia['message']}")
        else:
            print(f"Error al insertar la clase: {res_clase['message']}")

        # Confirmar todos los `INSERT` en la base de datos
        cursor.connection.commit()
        print("Operación completada: Todos los datos han sido guardados.")

    except Exception as e:
        cursor.connection.rollback()
        print(f"Ocurrió un error inesperado, revirtiendo cambios: {str(e)}")

    finally:
        cursor.connection.close()
