from back.db.operaciones.construir_db import construir_tablas
from unittest import TestCase, main
import sqlite3 as sqlite

TEST_DB = "test_database.db"
TABLAS = ["Imagenes", "Actividad",  "Sala", "Descuento", 
            "Pago", "Mensualidad", "Clase", "Pago_Pagar_Mensualidad", 
            "Pago_Pagar_Clase", "Usuario", "Clase_Tener_Mensualidad", 
            "Usuario_Cancelar_Clase", "Clase_Ocurrir_Sala", 
            "Usuario_Inscribir_Clase", "Usuario_Tener_Descuento"]

class EndpointTestCase(TestCase):
    """Test cases genérico para los endpoints."""
    def __init__(self):
        super().__init__()
        self.cursor = None
    
    def setUp(self):
        # Conectarse a la Base de Datos de prueba
        conexion = sqlite.connect(TEST_DB)
        conexion.row_factory = sqlite.Row

        # Crear el cursor y dejarlo como variable de la clase
        self.cursor = conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Si las tablas no fueron creadas aún
        construir_tablas(self.cursor)

    def tearDown(self):
        # Borrar información de cada tabla en la BD
        for tabla in TABLAS:
            self.cursor.execute(f"DELETE FROM {tabla};")
            print(f" > Se borraron las filas de la tabla {tabla}.")
