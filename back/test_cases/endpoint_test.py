from back.db.operaciones.construir_db import construir_tablas
from flask import Flask
from flask_cors import CORS
from unittest import TestCase, main
from routes import salas_bp

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
        self.client = None
        self.cursor = None
    
    def setUp(self):
        """Set up para el TestCase."""
        # Prender el puerto
        self.openTestPort()

        # Conectarse a la Base de Datos de prueba
        conexion = sqlite.connect(TEST_DB)
        conexion.row_factory = sqlite.Row

        # Crear el cursor y dejarlo como variable de la clase
        self.cursor = conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Si las tablas no fueron creadas aún
        construir_tablas(self.cursor)

    def tearDown(self):
        """Borrar información de cada tabla en la BD."""
        for tabla in TABLAS:
            self.cursor.execute(f"DELETE FROM {tabla};")
            print(f" > Se borraron las filas de la tabla {tabla}.")

    def openTestPort(self):
        """Se crea una app de Flask para probar los endpoints."""
        app = Flask(__name__)
        CORS(app)
        app.config['TESTING'] = True
        app.register_blueprint(salas_bp)
        self.client = app.test_client()
