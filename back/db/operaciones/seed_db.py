from db.operaciones.clase_tener_mensualidad.insertar_db import insertar_clase_tener_mensualidad
from db.operaciones.mensualidades.insertar_db import insertar_mensualidad
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones import insertar_pago, insertar_clase
from db.operaciones import insertar_pago_pagar_clase
from db.operaciones.instancias_clases.insertar_db import insertar_instancia_clase
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.usuarios.insertar_db import insertar_usuario_lista_espera_abonados, insertar_usuario_lista_espera_individual
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados, insertar_lista_espera_individual

# necesito insertarle mensualidades con actividades a los usuarios
def insertar_datos(cursor):  
    # Crear usuarios
    insertar_usuario(12345678, 'Juan', 'Pérez', '123333333', '2004-10-10', 'juan.perez@example.com', "1234",'M', 1, cursor)
    insertar_usuario(87654321, 'María', 'Gómez', '45644444', '2008-07-10', 'maria.gomez@example.com', "5678",'F', 3, cursor)
    insertar_usuario(39674828, 'Ernesto', 'Garcia', '12345678', '1997-07-10', 'ernesto.garcia@example.com', "5678",'M', 2, cursor)
    insertar_usuario(32031512, 'Lourdes', 'Gonzales', '6543713241', '1992-07-05', 'lourdes.gonzales@example.com', "5678",'F', 2, cursor)
    insertar_usuario(34673342, 'Gaspar', 'Solari', '7325466314', '2008-07-10', 'gaspar.solari@example.com', "5678",'M', 1, cursor)
   
    # Admin de prueba
    insertar_usuario(110101010, 'Admin', 'Ejemplo', '12345678', '2000-01-01', 'admin@gmail.com', "5678",'M', 1, cursor)

    # Usuario de prueba
    insertar_usuario(101010101, 'Usuario', 'Ejemplo', '12345678', '2000-01-01', 'usuario@yopmail.com', "5678",'M', 3, cursor)

    # Agregar 10 usuarios nuevos
    insertar_usuario(20000001, 'Lucia', 'Fernandez', '11111111', '1990-01-01', 'lucia.fernandez@yopmail.com', 'pwd01','F', 3, cursor)
    insertar_usuario(20000002, 'Mateo', 'Ramirez', '22222222', '1991-02-02', 'mateo.ramirez@yopmail.com', 'pwd02','M', 3, cursor)
    insertar_usuario(20000003, 'Sofia', 'Diaz', '33333333', '1992-03-03', 'sofia.diaz@yopmail.com', 'pwd03','F', 3, cursor)
    insertar_usuario(20000004, 'Diego', 'Vega', '44444444', '1993-04-04', 'diego.vega@yopmail.com', 'pwd04','M', 3, cursor)
    insertar_usuario(20000005, 'Valentina', 'Rios', '55555555', '1994-05-05', 'valentina.rios@yopmail.com', 'pwd05','F', 3, cursor)
    insertar_usuario(20000006, 'Nicolas', 'Suarez', '66666666', '1995-06-06', 'nicolas.suarez@yopmail.com', 'pwd06','M', 3, cursor)
    insertar_usuario(20000007, 'Isabella', 'Castro', '77777777', '1996-07-07', 'isabella.castro@yopmail.com', 'pwd07','F', 3, cursor)
    insertar_usuario(20000008, 'Lucas', 'Molina', '88888888', '1997-08-08', 'lucas.molina@yopmail.com', 'pwd08','M', 3, cursor)
    insertar_usuario(20000009, 'Camila', 'Ortiz', '99999999', '1998-09-09', 'camila.ortiz@yopmail.com', 'pwd09','F', 3, cursor)
    insertar_usuario(20000010, 'Joaquin', 'Herrera', '10101010', '1999-10-10', 'joaquin.herrera@yopmail.com', 'pwd10','M', 3, cursor)

    # Crear actividades
    insertar_actividad('Yoga', 50.0, cursor)
    insertar_actividad('Pilates', 60.0, cursor)
    insertar_actividad('Funcional', 70.0, cursor)

    # Crear solo usuarios comunes

    # Crear profesores
    id_prof1 = insertar_profesor('Carlos', 'López', '542215004012', 'M', 11223344, [1, 2], cursor)
    insertar_profesor('Ana', 'Martínez', '542215004013','F', 44332211, [1], cursor)

    id_prof1 = id_prof1['data']

    insertar_mensualidad('2026-01-01', '2026-12-01', 1, cursor)
    insertar_mensualidad('2026-02-02', '2026-12-02', 2, cursor)

    # Crear roles
    insertar_rol('Administrador', cursor)
    insertar_rol('Recepcionista', cursor)
    
    # Crear salas
    insertar_sala('Sala 1', 10, cursor)
    insertar_sala('Sala 2', 25, cursor)
    insertar_sala('Sala 3', 5, cursor)

    # Crear clase
    id_clas = insertar_clase('Programada', 1, id_prof1, 1, "Lunes", "10:00", 5, 300.0, cursor)
    id_clas = id_clas['data']
    res_inst_clase = insertar_instancia_clase(id_clas, '2026-06-01', 200.0, cursor)
    
    # Crear listas de espera para la clase
    inst_clase_id = res_inst_clase['data']
    id_lea = insertar_lista_espera_abonados(id_clas, cursor)["data"]
    id_lei = insertar_lista_espera_individual(inst_clase_id, cursor)["data"]

    # Inscribir usuario a clase
    insertar_reserva(1, inst_clase_id, cursor)
    insertar_usuario_lista_espera_abonados(id_lea, 2, cursor)
    insertar_usuario_lista_espera_individual(id_lei, 4, cursor)

    # Crear pagos
    insertar_pago(50.0, 1, cursor)
    insertar_pago(60.0, 2, cursor)

    # Crear pagos pagar clase
    insertar_pago_pagar_clase(1, 1, cursor)

    # Crear una clase adicional programada para martes y su instancia (martes)
    id_clas_martes = insertar_clase('Programada Martes', 1, id_prof1, 2, "Martes", "11:00", 8, 1000.0, cursor)
    id_clas_martes = id_clas_martes['data']
    # Fecha ejemplo que corresponde a un martes
    insertar_instancia_clase(id_clas_martes, '2026-06-02', 100.0, cursor)

    insertar_clase_tener_mensualidad(2, 2, cursor)
    
    insertar_instancia_clase(2, '2026-11-03', 1500.0, cursor)