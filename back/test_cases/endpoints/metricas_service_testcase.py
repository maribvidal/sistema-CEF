from ..endpoint_test import EndpointTestCase
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.instancias_clases.insertar_db import insertar_instancia_clase
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.salas.insertar_db import insertar_sala
from db.operaciones.usuarios.insertar_db import insertar_usuario

class MetricasServiceTestCase(EndpointTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def _insertar_cancelacion(self, fecha, usuario_id, inst_clase_id):
        self.cursor.execute(
            "INSERT INTO Cancelacion (fecha, usuario_id, inst_clase_id) VALUES (?, ?, ?);",
            (fecha, usuario_id, inst_clase_id)
        )

    def _armar_escenario_con_cancelaciones(self):
        id_profesor = insertar_profesor("Ana", "Perez", "F", 20111222, self.cursor)["data"]

        id_usuario_1 = insertar_usuario(
            41298622,
            "Mariano",
            "Venal",
            "12345678",
            "2004-02-02",
            "mariano1@example.com",
            "542215253779",
            "M",
            1,
            self.cursor
        )["data"]
        id_usuario_2 = insertar_usuario(
            41298623,
            "Sofia",
            "Lorenzo",
            "12345678",
            "2004-03-03",
            "sofia1@example.com",
            "542215253780",
            "F",
            1,
            self.cursor
        )["data"]

        id_actividad_yoga = insertar_actividad("Yoga", 1250, self.cursor)["data"]
        id_actividad_pilates = insertar_actividad("Pilates", 1500, self.cursor)["data"]
        id_sala = insertar_sala("Sala 1", 10, self.cursor)["data"]

        id_clase_yoga = insertar_clase(
            "Activa",
            id_actividad_yoga,
            id_profesor,
            id_sala,
            "Lunes",
            "10:00",
            10,
            300.0,
            self.cursor
        )["data"]
        id_clase_pilates = insertar_clase(
            "Activa",
            id_actividad_pilates,
            id_profesor,
            id_sala,
            "Martes",
            "12:00",
            10,
            400.0,
            self.cursor
        )["data"]

        id_inst_yoga = insertar_instancia_clase(id_clase_yoga, "2026-06-10", 150.0, self.cursor)["data"]
        id_inst_pilates = insertar_instancia_clase(id_clase_pilates, "2026-06-11", 200.0, self.cursor)["data"]

        self._insertar_cancelacion("2026-06-01", id_usuario_1, id_inst_yoga)
        self._insertar_cancelacion("2026-06-03", id_usuario_2, id_inst_yoga)
        self._insertar_cancelacion("2026-06-05", id_usuario_1, id_inst_yoga)

        self._insertar_cancelacion("2026-06-02", id_usuario_1, id_inst_pilates)
        self._insertar_cancelacion("2026-06-04", id_usuario_2, id_inst_pilates)

        self.cursor.connection.commit()

        return {
            "id_actividad_yoga": id_actividad_yoga,
            "id_actividad_pilates": id_actividad_pilates,
            "id_inst_yoga": id_inst_yoga,
            "id_inst_pilates": id_inst_pilates
        }
        
    def test_no_hay_cancelaciones(self):

        res = self.client.get(
            "/metricas/clases_mas_canceladas",
            query_string={
                "limite": 5
            }
        )

        json_res = self.decodificarRespByte(res.data)

        assert res.status_code == 400
        assert json_res["error"] == "No se encontraron clases canceladas."

    def test_listar_clases_mas_canceladas_con_datos(self):
        self._armar_escenario_con_cancelaciones()

        res = self.client.get(
            "/metricas/clases_mas_canceladas",
            query_string={
                "limite": 5
            }
        )

        json_res = self.decodificarRespByte(res.data)

        assert res.status_code == 200
        assert len(json_res) == 2
        assert json_res[0]["actividad"] == "Yoga"
        assert json_res[0]["cancelaciones"] == 3
        assert json_res[1]["actividad"] == "Pilates"
        assert json_res[1]["cancelaciones"] == 2

    def test_filtra_por_actividad_y_fechas(self):
        datos = self._armar_escenario_con_cancelaciones()

        res = self.client.get(
            "/metricas/clases_mas_canceladas",
            query_string={
                "limite": 5,
                "id_actividad": datos["id_actividad_yoga"],
                "fecha_inicio": "2026-06-02",
                "fecha_fin": "2026-06-04"
            }
        )

        json_res = self.decodificarRespByte(res.data)

        assert res.status_code == 200
        assert len(json_res) == 1
        assert json_res[0]["actividad"] == "Yoga"
        assert json_res[0]["cancelaciones"] == 1
    