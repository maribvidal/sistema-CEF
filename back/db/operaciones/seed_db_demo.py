from db.operaciones.asistencias.insertar_db import registrar_asistencia
from db.operaciones.pago_pagar_mensualidad.insertar_db import insertar_pago_pagar_mensualidad
from db.operaciones.clase_tener_mensualidad.insertar_db import insertar_clase_tener_mensualidad
from db.operaciones.cancelaciones.insertar_db import insertar_cancelacion
from db.operaciones.mensualidades.insertar_db import insertar_mensualidad, insertar_mensualidad_con_fin
from db.operaciones.usuarios.insertar_db import insertar_usuario, insertar_usuario_verificado
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones import insertar_pago, insertar_clase
from db.operaciones import insertar_pago_pagar_clase
from db.operaciones.instancias_clases.insertar_db import insertar_instancia_clase, crear_instancias_clase_por_un_año
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.usuarios.insertar_db import insertar_usuario_lista_espera_abonados, insertar_usuario_lista_espera_individual
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados, insertar_lista_espera_individual
from utils.modulo_fechas import generar_fecha_actual

def insertar_datos(cursor):  

    # Crear roles

    insertar_rol('Administrador', cursor)
    insertar_rol('Recepcionista', cursor)


    # Crear usuarios
    insertar_usuario_verificado(12345678, 'Juan', 'Pérez', '12345678', '2004-10-10', 'admin1@gmail.com', "1234",'M', 1, cursor)
    insertar_usuario_verificado(87654321, 'María', 'Gómez', '12345678', '2008-07-10', 'admin2@gmail.com', "5678",'F', 1, cursor)
    insertar_usuario_verificado(39674828, 'Ernesto', 'Garcia', '12345678', '1997-07-10', 'recep1@gmail.com', "5678",'M', 2, cursor)
    insertar_usuario_verificado(32031512, 'Lourdes', 'Gonzales', '12345678', '1992-07-05', 'recep2@gmail.com', "5678",'F', 2, cursor)
    insertar_usuario_verificado(34673342, 'Gaspar', 'Solari', '12345678', '2008-07-10', 'user1@gmail.com', "5678",'M', 3, cursor)
    insertar_usuario_verificado(20000001, 'Lucia', 'Fernandez', '12345678', '1990-01-01', 'user2@gmail.com', '7777','F', 3, cursor)
    insertar_usuario_verificado(20000002, 'Mateo', 'Ramirez', '12345678', '1991-02-02', 'user3@gmail.com', '8888','M', 3, cursor)
    insertar_usuario_verificado(11111111, 'Sofia', 'Diaz', '12345678', '1992-03-03', 'user4@gmail.com', '9999','F', 3, cursor)

# Crear actividades
    insertar_actividad('Yoga', 50.0, cursor)
    insertar_actividad('Pilates', 60.0, cursor)
    insertar_actividad('Funcional', 70.0, cursor)
# Profesores
    id_prof1 = insertar_profesor('Carlos', 'López', '542215004012', 'M', 11223344, [1, 2], cursor)
    insertar_profesor('Ana', 'Martínez', '542215004013','F', 44332211, [1], cursor)    

    id_prof1 = id_prof1['data']
    # Crear salas
    insertar_sala('Sala 1', 10, cursor)
    insertar_sala('Sala 2', 25, cursor)
    insertar_sala('Sala 3', 5, cursor)

    # Crear clases
    id_clas = insertar_clase('Programada', 1, id_prof1, 1, "Lunes", "10:00", 1, 300.0, cursor)
    lista_ids_cla_1 = crear_instancias_clase_por_un_año(id_clas, 300, cursor, "Lunes")
    for idi in lista_ids_cla_1:
        insertar_lista_espera_individual(idi, cursor)
    
    
    # Crear la lista de espera de abonados para la clase
    inst_clase_id = lista_ids_cla_1[0]
    id_lea = insertar_lista_espera_abonados(id_clas, cursor)["data"]

    # Inscribir usuario a clase
    insertar_reserva(5, inst_clase_id, cursor)

    # Crear pagos
    insertar_pago(50.0, 5, cursor)
    insertar_pago(60.0, 5, cursor)
    insertar_pago(70.0, 5, cursor)

    # Crear pagos pagar clase
    insertar_pago_pagar_clase(1, 1, cursor)
    
    insertar_pago_pagar_mensualidad(2, 1, cursor)
    insertar_pago_pagar_mensualidad(3, 1, cursor)
    
    insertar_clase_tener_mensualidad(1, 1, cursor)


    insertar_cancelacion(5, lista_ids_cla_1[0], cursor)
    insertar_cancelacion(5, lista_ids_cla_1[0], cursor)

