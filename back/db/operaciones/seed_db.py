from db.operaciones.mensualidades.insertar_db import insertar_mensualidad
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.permisos.insertar_db import insertar_permiso
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones import insertar_pago, insertar_clase
from db.operaciones import insertar_pago_pagar_clase
from db.operaciones.instancias_clases.insertar_db import insertar_instancia_clase
from db.operaciones.reservas.insertar_db import insertar_reserva

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
    id_clas = insertar_clase('Programada', 1, id_prof1, 1, "Lunes", "10:00", 5, cursor)
    id_clas = id_clas['data']
    res_inst_clase = insertar_instancia_clase(id_clas, 1, 'Domingo', '10:00', cursor)
    
    # Inscribir usuario a clase
    inst_clase_id = res_inst_clase['data']
    insertar_reserva(1, inst_clase_id, cursor)

    # Crear pagos
    insertar_pago(50.0, 1, cursor)
    insertar_pago(60.0, 2, cursor)

    # Crear pagos pagar clase
    insertar_pago_pagar_clase(1, 1, cursor)
