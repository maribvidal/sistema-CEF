from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.permisos.insertar_db import insertar_permiso
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones.clase_ocurrir_sala.insertar_db import insertar_clase_ocurrir_sala
from db.operaciones import insertar_pago, insertar_clase
from db.operaciones import insertar_pago_pagar_clase

def insertar_datos(cursor):  
    # Crear usuarios
    insertar_usuario(12345678, 'Juan', 'Pérez', '123', '2004-10-10', 'juan.perez@example.com', "1234",'M', 1, cursor)
    insertar_usuario(87654321, 'María', 'Gómez', '456', '2008-07-10', 'maria.gomez@example.com', "5678",'F', 3, cursor)
    
    # Crear profesores
    insertar_profesor('Carlos', 'López', 'M', 11223344, cursor)
    insertar_profesor('Ana', 'Martínez', 'F', 44332211, cursor)

    # Crear actividades
    insertar_actividad('Yoga', 50.0, cursor)
    insertar_actividad('Pilates', 60.0, cursor)
    insertar_actividad('Funcional', 70.0, cursor)

    #insertar_mensualidad('2024-01-01', '2024-31-01', 1)
    #insertar_mensualidad('2024-02-02', '2024-29-02', 2)

    # Crear permisos
    insertar_permiso('Metricas', cursor)

    # Crear roles
    insertar_rol('Administrador', cursor)
    insertar_rol('Recepcionista', cursor)
    
    # Crear salas
    insertar_sala('Sala 1', cursor)
    insertar_sala('Sala 2', cursor)
    insertar_sala('Sala 3', cursor)

    # Crear clase
    insertar_clase('Programada', 1, 1, cursor)
    insertar_clase_ocurrir_sala(1, 1, '2024-07-01', "10:00", cursor)

    # Crear pagos
    insertar_pago(50.0, 1, cursor)
    insertar_pago(60.0, 2, cursor)

    # Crear pagos pagar clase
    insertar_pago_pagar_clase(1, 1, cursor)
