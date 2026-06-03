from db.operaciones.construir_db import construir_tablas
from flask import Flask
from flask_cors import CORS
from unittest import TestCase, main
from app import create_app

import json
import os
import sqlite3 as sqlite

TEST_DB = "test_database.db"

class EndpointTestCase(TestCase):
    """Test cases genérico para los endpoints."""
    def setUp(self):
        """Set up para el TestCase."""
        # Prender el puerto
        self.openTestPort()
        print(" > TESTING / Abriendo el puerto 5000")

        # Conectarse a la Base de Datos de prueba
        conexion = sqlite.connect(TEST_DB)
        conexion.row_factory = sqlite.Row
        print(" > TESTING / Creando la conexión con 'test_database.db'")

        # Crear el cursor y dejarlo como variable de la clase
        self.cursor = conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Si las tablas no fueron creadas aún
        construir_tablas(self.cursor)
        print(" > TESTING / Creando tablas en 'test_database.db'")

    def tearDown(self):
        """Borrar BD."""
        self.cursor.connection.close()
        print(" > TESTING / Cerrando la conexión")
        os.remove(TEST_DB)
        print(" > TESTING / Borrando 'test_database.db'")

    def openTestPort(self):
        """Se crea una app de Flask para probar los endpoints."""
        self.client = create_app(testing=True, db_name=TEST_DB).test_client()

    def decodificarRespByte(self, resp: bytes):
        resp_json = resp.decode('utf8').replace("'", '"')
        data = json.loads(resp_json)
        return data
