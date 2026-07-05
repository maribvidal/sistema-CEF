from ..endpoint_test import EndpointTestCase

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

from services.mensualidad_service import verificar_mensualidades_por_vencer

class MensualidadesTestCase(EndpointTestCase):
    """Testcase para probar las mensualidades."""
    def setUp(self):
        print(" > TESTING / TESTCASE DE LAS MENSUALIDADES")
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_probar_vencimiento_mensualidad(self):
        # Crear usuarios
        insertar_usuario_verificado(12345678, 'Juan', 'Pérez', '123333333', '2004-10-10', 'juan.perez@example.com', "1234",'M', 1, self.cursor)
        insertar_usuario_verificado(87654321, 'María', 'Gómez', '45644444', '2008-07-10', 'maria.gomez@example.com', "5678",'F', 3, self.cursor)
        insertar_usuario_verificado(39674828, 'Ernesto', 'Garcia', '12345678', '1997-07-10', 'ernesto.garcia@example.com', "5678",'M', 2, self.cursor)
        insertar_usuario_verificado(32031512, 'Lourdes', 'Gonzales', '6543713241', '1992-07-05', 'lourdes.gonzales@example.com', "5678",'F', 2, self.cursor)
        insertar_usuario_verificado(34673342, 'Gaspar', 'Solari', '7325466314', '2008-07-10', 'gaspar.solari@example.com', "5678",'M', 1, self.cursor)

        # Agregar 10 usuarios nuevos
        usu_1 = insertar_usuario_verificado(20000001, 'Lucia', 'Fernandez', '11111111', '1990-01-01', 'lucia.fernandez@yopmail.com', 'pwd01','F', 3, self.cursor)
        insertar_usuario_verificado(20000002, 'Mateo', 'Ramirez', '22222222', '1991-02-02', 'mateo.ramirez@yopmail.com', 'pwd02','M', 3, self.cursor)
        id_usu_1 = usu_1["data"]

        # Crear actividades
        insertar_actividad('Yoga', 50.0, self.cursor)
        insertar_actividad('Pilates', 60.0, self.cursor)
        insertar_actividad('Funcional', 70.0, self.cursor)

        # Crear profesores
        id_prof1 = insertar_profesor('Carlos', 'López', '542215004012', 'M', 11223344, [1, 2], self.cursor)['data']
        id_prof2 = insertar_profesor('Ana', 'Martínez', '542215004013','F', 44332211, [1], self.cursor)['data']

        insertar_mensualidad(1, self.cursor, '2026-01-01')
        insertar_mensualidad(2, self.cursor, '2026-02-02')

        # Crear roles
        insertar_rol('Administrador', self.cursor)
        insertar_rol('Recepcionista', self.cursor)
        
        # Crear salas
        insertar_sala('Sala 1', 10, self.cursor)
        insertar_sala('Sala 2', 25, self.cursor)
        insertar_sala('Sala 3', 5, self.cursor)

        # Crear clase
        id_clas = insertar_clase('Programada', 1, id_prof1, 1, "Lunes", "10:00", 0, 300.0, self.cursor)
        id_clas = id_clas['data']
        lista_ids_cla_1 = crear_instancias_clase_por_un_año(id_clas, 300, self.cursor, "Lunes")
        # Crear listas de espera individuales
        for idi in lista_ids_cla_1:
            insertar_lista_espera_individual(idi, self.cursor)
        
        # Crear la lista de espera de abonados para la clase
        inst_clase_id = lista_ids_cla_1[0]
        id_lea = insertar_lista_espera_abonados(id_clas, self.cursor)["data"]

        # Inscribir usuario a clase
        insertar_reserva(1, inst_clase_id, self.cursor)
        insertar_usuario_lista_espera_abonados(id_lea, 2, self.cursor)
        insertar_usuario_lista_espera_individual(lista_ids_cla_1[0], 4, self.cursor)

        # Datos para probar el scheduler de notificaciones
        mensualidad = insertar_mensualidad_con_fin(id_usu_1, self.cursor, '2026-06-02', '2026-07-01')
        
        id_clas_martes = insertar_clase('Programada', 2, id_prof2, 1, "Miércoles", "18:00", 12, 550.0, self.cursor)
        id_clas_martes = id_clas_martes['data']
        inst_clase_martes = insertar_instancia_clase(id_clas_martes, '2026-07-01', 550.0, self.cursor)
        inst_clase_martes = insertar_instancia_clase(id_clas_martes, '2026-07-10', 550.0, self.cursor)
        inst_clase_martes = insertar_instancia_clase(id_clas_martes, '2026-09-10', 550.0, self.cursor)

        self.cursor.connection.commit()

        # Verificar mensualidades vencidas
        verificar_mensualidades_por_vencer(self.cursor)
    