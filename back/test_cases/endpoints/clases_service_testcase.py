from .. import EndpointTestCase

class ClasesServiceTestCase(EndpointTestCase):
    """Testcase para probar los endpoints del service de Clases."""
    def setUp(self):
        super().setUp()
        print(" >> Comenzando TestCase para el service de Clases.")

    def tearDown(self):
        print(" >> Terminando TestCase para el service de Clases.")
        super().tearDown()

    def test_listar_clases(self):
        ### ESCENARIO 1: Clases listadas con éxito
        # Crear profesores
        id_prof1 = insertar_profesor("Gero", "Arias", "M", "22224444", self.cursor)
        id_prof2 = insertar_profesor("Malena", "Bancos", "F", "23234545", self.cursor)

        # Crear actividades
        id_act1 = insertar_actividad("Musculatura", 1250, self.cursor)
        id_act2 = insertar_actividad("Funcional", 1500, self.cursor)

        # Crear clases
        id_cla1 = insertar_clase("Activa", id_act1, id_prof1, 10, self.cursor)
        id_cla2 = insertar_clase("Activa", id_act2, id_prof2, 5, self.cursor)

        # Probar endpoint "listar_clases"
        res, code = self.client.get("/clases")

        assert res.status == "Success", "La respuesta no es 'success'."
        assert code == 200, "El código de éxito no es igual a 200."
        assert res.data[0].id == id_cla1, f"El id de la primera clase insertada es distinto de {id_cla1}."
        assert res.data[0].estado == "Activa", f"El estado de la primera clase insertada es distinto de 'Activa'."
        assert res.data[0].actividad_id == id_act1, f"El id de la actividad de la primera clase insertada es distinto de {id_act1}."
        assert res.data[0].profesor_id == id_prof1, f"El id del profesor de la primera clase insertada es distinto de {id_prof1}."
        assert res.data[0].cupo_maximo == 10, f"El cupo máximo de la primera clase insertada es distinto de 10."

        ### ESCENARIO 2: Error en listado de clases 
    