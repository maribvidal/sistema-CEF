
class ClasesServiceTestCase(EndpointTestCase):
    """Testcase para probar los endpoints del service de Usuarios."""
    def setUp(self):
        super().setUp()
        print(" > TESTING / Comenzando TestCase para el service de Usuarios.")

    def tearDown(self):
        super().tearDown()
        print(" > TESTING / Terminando TestCase para el service de Usuarios.")
