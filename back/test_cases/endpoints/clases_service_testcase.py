from ..endpoint_test import EndpointTestCase
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clase_ocurrir_sala.insertar_db import insertar_clase_ocurrir_sala
from db.operaciones.salas.insertar_db import insertar_sala

class ClasesServiceTestCase(EndpointTestCase):
    """Testcase para probar los endpoints del service de Clases."""
    def setUp(self):
        super().setUp()
        print(" > TESTING / Comenzando TestCase para el service de Clases.")

    def tearDown(self):
        super().tearDown()
        print(" > TESTING / Terminando TestCase para el service de Clases.")

    def test_listar_clases_solas(self):
        ### ESCENARIO 2: Error en listado de clases
        res = self.client.get("/clase")

        json_res = self.decodificarRespByte(res.data)
        info = list(json_res)[0]

        assert info == 'error', "No habían clases cargadas y no se tiró error."
        assert '401' in str(res), "El código devuelto no es 401."

        ### ESCENARIO 1: Clases listadas con éxito
        # Crear profesores
        id_prof1 = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)["data"]
        id_prof2 = insertar_profesor("Malena", "Bancos", "F", "23234545", self.cursor)["data"]

        # Crear actividades
        id_act1 = insertar_actividad("Musculatura", 1250, self.cursor)["data"]
        id_act2 = insertar_actividad("Funcional", 1500, self.cursor)["data"]

        # Crear clases
        id_cla1 = insertar_clase("Activa", id_act1, id_prof1, 10, self.cursor)["data"]
        id_cla2 = insertar_clase("Activa", id_act2, id_prof2, 5, self.cursor)["data"]

        self.cursor.connection.commit()

        # Probar endpoint "listar_clases_sin_info_extra"
        res = self.client.get("/clase")

        json_res = self.decodificarRespByte(res.data)
        json_status = json_res["status"]
        json_primera_clase = json_res["data"][0]

        assert '200' in str(res), "El código devuelto no es 200."
        assert json_status == 'success', "La respuesta no es 'success'."
        assert json_primera_clase["id"] == id_cla1, f"El id de la primera clase insertada es distinto de {id_cla1}."
        assert json_primera_clase["estado"] == 'Activa', "El estado de la primera clase insertada es distinto de 'Activa'."
        assert json_primera_clase["actividad_id"] == id_act1, f"El id de la actividad de la primera clase insertada es distinto de {id_act1}."
        assert json_primera_clase["profesor_id"] == id_prof1, f"El id del profesor de la primera clase insertada es distinto de {id_prof1}."
        assert json_primera_clase["cupo_maximo"] == 10, "El cupo máximo de la primera clase insertada es distinto de 10."
    
    def test_listar_clases(self):
        ### ESCENARIO 2: Error en listado de clases
        res = self.client.get("/clases")

        json_res = self.decodificarRespByte(res.data)
        info = list(json_res)[0]

        assert info == 'error', "No habían clases cargadas y no se tiró error."
        assert '401' in str(res), "El código devuelto no es 401."

        ### ESCENARIO 1: Clases listadas con éxito
        # Crear profesores
        id_prof1 = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)["data"]
        id_prof2 = insertar_profesor("Malena", "Bancos", "F", "23234545", self.cursor)["data"]

        # Crear actividades
        id_act1 = insertar_actividad("Musculatura", 1250, self.cursor)["data"]
        id_act2 = insertar_actividad("Funcional", 1500, self.cursor)["data"]

        # Crear clases
        id_cla1 = insertar_clase("Activa", id_act1, id_prof1, 10, self.cursor)["data"]
        id_cla2 = insertar_clase("Activa", id_act2, id_prof2, 5, self.cursor)["data"]

        # Crear salas
        id_sala1 = insertar_sala("Sala 1", 10, self.cursor)["data"]
        id_sala2 = insertar_sala("Sala 2", 10, self.cursor)["data"]

        # Crear clase_ocurrir_sala
        id_cos1 = insertar_clase_ocurrir_sala(id_cla1, id_sala1, "Lunes", "10:00", self.cursor)["data"]
        id_cos2 = insertar_clase_ocurrir_sala(id_cla2, id_sala2, "Martes", "12:00", self.cursor)["data"]

        self.cursor.connection.commit()

        # Probar endpoint "listar_clases_sin_info_extra"
        res = self.client.get("/clases")

        json_res = self.decodificarRespByte(res.data)
        json_status = json_res["status"]
        json_primera_clase = json_res["data"][0]

        assert '200' in str(res), "El código devuelto no es 200."
        assert json_status == 'success', "La respuesta no es 'success'."
        assert len(json_res["data"]) == 2, f"Se esperaban 2 clases, pero se encontraron {len(json_res['data'])}."
        assert json_primera_clase["id"] == id_cla1, f"El id de la primera clase insertada es distinto de {id_cla1}."
        assert json_primera_clase["estado"] == 'Activa', "El estado de la primera clase insertada es distinto de 'Activa'."
        assert json_primera_clase["actividad_id"] == id_act1, f"El id de la actividad de la primera clase insertada es distinto de {id_act1}."
        assert json_primera_clase["profesor_id"] == id_prof1, f"El id del profesor de la primera clase insertada es distinto de {id_prof1}."
        assert json_primera_clase["cupo_maximo"] == 10, "El cupo máximo de la primera clase insertada es distinto de 10."
        assert json_primera_clase["fecha"] == '2026-12-07', "La fecha es distinta a la ingresada."
        assert json_primera_clase["hora"] == '10:00', "La hora es distinta a la ingresada."
        assert json_primera_clase["sala_id"] == 1, "La sala es distinta a la ingresada."
