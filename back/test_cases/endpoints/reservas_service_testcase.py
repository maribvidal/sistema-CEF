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

class ReservasServiceTestcase(EndpointTestCase):
    """Testcase para probar el service de Reservas."""
    def setUp(self):
        print(" > TESTING / TESTCASE DEL SERVICE DE RESERVA")
        super().setUp()

    def tearDown(self):
        super().tearDown()
