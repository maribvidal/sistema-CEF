from ..endpoint_test import EndpointTestCase

from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.clases import insertar_clase, consultar_clase_por_id
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.instancias_clases import insertar_instancia_clase, consultar_instancia_clase_por_clase_id
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.reservas.insertar_db import insertar_reserva
from db.operaciones.listas_espera.insertar_db import insertar_lista_espera_abonados, insertar_lista_espera_individual
from db.operaciones.usuarios.insertar_db import insertar_usuario_lista_espera_abonados, insertar_usuario_lista_espera_individual

from utils.modulo_manejo_listas import manejar_listas_de_espera_por_clase
from utils.modulo_fechas import generar_fecha_hora_actual

class ListasEsperaTestcase(EndpointTestCase):
    """Testcase para probar el mecanismo de la listas de espera."""
    def setUp(self):
        print(" > TESTING / TESTCASE DE LAS LISTAS DE ESPERA")
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_manejo_lista_espera(self):
        # Crear profesores
        id_prof1 = insertar_profesor("Gero", "Arias", "542215253770", "M", "22224444", self.cursor)["data"]
        id_prof2 = insertar_profesor("Malena", "Bancos", "542215253722", "F", "23234545", self.cursor)["data"]

        # Crear actividades
        id_act1 = insertar_actividad("Musculatura", 1250, self.cursor)["data"]
        id_act2 = insertar_actividad("Funcional", 1500, self.cursor)["data"]

        # Crear salas
        id_sala1 = insertar_sala("Sala 1", 10, self.cursor)["data"]
        id_sala2 = insertar_sala("Sala 2", 10, self.cursor)["data"]

        # Crear clases
        id_cla1 = insertar_clase("Activa", id_act1, id_prof1, id_sala1, "Lunes", "10:00", 3, 300.0, self.cursor)["data"]
        id_cla2 = insertar_clase("Activa", id_act2, id_prof2, id_sala2, "Martes", "12:00", 3, 400.0, self.cursor)["data"]

        # Crear instancia_clase
        id_ic1 = insertar_instancia_clase(id_cla1, "2026-12-02", 100.0, self.cursor)["data"]
        id_ic2 = insertar_instancia_clase(id_cla1, "2026-02-02", 150.0, self.cursor)["data"]
        id_ic3 = insertar_instancia_clase(id_cla2, "2026-12-03", 200.0, self.cursor)["data"]
        id_ic4 = insertar_instancia_clase(id_cla2, "2026-02-03", 250.0, self.cursor)["data"]

        # Crear usuarios
        id_usuarios_reservaron = []
        for i in range(0, 2):
            id_cli_nuevo = insertar_usuario(f"40123412{i}", "Cliente", f"N°{i}", "12345678", generar_fecha_hora_actual(), f"cef_cli{i}@yopmail.com", "542215253772", "M", 3, self.cursor)["data"]
            id_cli_nuevo2 = insertar_usuario(f"5012301{i}", "Cliente", f"N°{i+2}", "12345678", generar_fecha_hora_actual(), f"cef_cli{i+2}@gmail.com", "542215253773", "F", 3, self.cursor)["data"]
            insertar_reserva(id_cli_nuevo, id_ic1, self.cursor)
            insertar_reserva(id_cli_nuevo2, id_ic3, self.cursor)
            id_usuarios_reservaron.append(id_cli_nuevo)
            id_usuarios_reservaron.append(id_cli_nuevo2)
        for i in range(0, 2):
            id_cli_nuevo = insertar_usuario(f"30123412{i}", "Cliente", f"N°{i+4}", "12345678", generar_fecha_hora_actual(), f"cef_cli{i+4}@yopmail.com", "542215253774", "M", 3, self.cursor)["data"]
            id_cli_nuevo2 = insertar_usuario(f"2012301{i}", "Cliente", f"N°{i+6}", "12345678", generar_fecha_hora_actual(), f"cef_cli{i+6}@yopmail.com", "542215253775", "F", 3, self.cursor)["data"]
            insertar_reserva(id_cli_nuevo, id_ic2, self.cursor)
            insertar_reserva(id_cli_nuevo2, id_ic4, self.cursor)
            id_usuarios_reservaron.append(id_cli_nuevo)
            id_usuarios_reservaron.append(id_cli_nuevo2) 

        id_usuarios_esperando = []
        for i in range(0, 3):
            id_cli_nuevo = insertar_usuario(f"80123412{i}", "Cliente", f"N°{i+8}", "12345678", generar_fecha_hora_actual(), f"cef_cli{i}@yopmail.com", "542215253776", "M", 3, self.cursor)["data"]
            id_cli_nuevo2 = insertar_usuario(f"7012301{i}", "Cliente", f"N°{i+11}", "12345678", generar_fecha_hora_actual(), f"cef_cli{i+2}@yopmail.com", "542215253777", "F", 3, self.cursor)["data"]
            id_usuarios_esperando.append(id_cli_nuevo)
            id_usuarios_esperando.append(id_cli_nuevo2)

        self.cursor.connection.commit()

        # Crear listas de espera y meter a los dos usuarios anteriormente creados
        id_lea1 = insertar_lista_espera_abonados(id_cla1, self.cursor)["data"]
        id_lei1 = insertar_lista_espera_individual(id_ic1, self.cursor)["data"]
        id_lei2 = insertar_lista_espera_individual(id_ic2, self.cursor)["data"]
        id_lea2 = insertar_lista_espera_abonados(id_cla2, self.cursor)["data"]
        id_lei3 = insertar_lista_espera_individual(id_ic3, self.cursor)["data"]
        id_lei4 = insertar_lista_espera_individual(id_ic4, self.cursor)["data"]

        self.cursor.connection.commit()

        print("Listas vacías")
        print(manejar_listas_de_espera_por_clase(1, self.cursor))
        print(manejar_listas_de_espera_por_clase(2, self.cursor))

        # Meter a un usuario en cada lista de abonados
        insertar_usuario_lista_espera_abonados(id_lea1, id_usuarios_esperando[1], self.cursor)
        insertar_usuario_lista_espera_abonados(id_lea2, id_usuarios_esperando[2], self.cursor)
        insertar_usuario_lista_espera_abonados(id_lea2, id_usuarios_esperando[3], self.cursor)

        self.cursor.connection.commit()

        print("Listas de abonados con gente")
        print(manejar_listas_de_espera_por_clase(1, self.cursor))
        print(manejar_listas_de_espera_por_clase(2, self.cursor))

        # Meter a un usuario en cada lista de espera individual
        insertar_usuario_lista_espera_individual(id_lei1, id_usuarios_esperando[4], self.cursor)
        insertar_usuario_lista_espera_individual(id_lei2, id_usuarios_esperando[5], self.cursor)
        insertar_usuario_lista_espera_individual(id_lei3, id_usuarios_esperando[0], self.cursor)

        self.cursor.connection.commit()

        print("Todas las listas con gente")
        print(manejar_listas_de_espera_por_clase(1, self.cursor))
        print(manejar_listas_de_espera_por_clase(2, self.cursor))
