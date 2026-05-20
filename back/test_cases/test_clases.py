import unittest

from db.operaciones_consulta_comunes import consultar_clase_por_id
from db.operaciones_insercion_comunes import crear_actividad, crear_profesor, publicar_clase

class ClasesTestcase(unittest.TestCase):
    """Clase test para probar las operaciones de la BD
        relacionadas con las clases."""
    
    def setUp(self):
        """Fixture para las pruebas."""
        print(" - Iniciando test de clases...")

    def tearDown(self):
        """Fixture para terminar las pruebas."""
        print(" - Test de clases finalizado.")

    def test_publicar_clase(self):
        """Este test verifica que se pueda publicar una clase 
            sin errores."""
        
        crear_actividad('Funcional', 150.0)
        crear_profesor('Gero', 'Arias', 'M', 6656342)
        res = publicar_clase('programada', 1, 1)
        self.assertNotEqual(res, -1,
                    "Error al publicar la clase: se devolvió -1")
        tupla_clase = consultar_clase_por_id(res)
        self.assertEqual(tupla_clase[1], 'programada')
        self.assertIsNotNone(tupla_clase, "Error al consultar la clase: se devolvió None")

"""

    def test_fetch_missing_user(self):
        # Debe devolver None si el registro no existe.
        self.cursor.execute('SELECT id FROM users WHERE name = ?', ('Bob',))
        row = self.cursor.fetchone()
        self.assertIsNone(row)

    def test_insert_user_no_exception(self):
        # Operación que debe funcionar sin lanzar excepción.
        self.cursor.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            ('Bob', 'bob@example.com'),
        )
        self.connection.commit()
        self.cursor.execute('SELECT COUNT(*) FROM users')
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 2)

    def test_update_user_no_exception(self):
        # Otra operación para comprobar que no hay excepciones.
        self.cursor.execute(
            'UPDATE users SET email = ? WHERE name = ?',
            ('alice@newdomain.com', 'Alice'),
        )
        self.connection.commit()
        self.cursor.execute('SELECT email FROM users WHERE name = ?', ('Alice',))
        email = self.cursor.fetchone()[0]
        self.assertEqual(email, 'alice@newdomain.com')
"""

if __name__ == '__main__':
    unittest.main()
