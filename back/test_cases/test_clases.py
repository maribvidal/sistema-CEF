import unittest

from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones_consulta_comunes import consultar_clase_por_id
from db.operaciones_insercion_comunes import crear_actividad, crear_profesor, publicar_clase
from db.operaciones_eliminar_comunes import eliminar_clase_por_id
from db.operaciones_modificar_comunes import modificar_clase

class ClasesTestcase(unittest.TestCase):
    """Clase test para probar las operaciones de la BD
        relacionadas con las clases."""
    
    def setUp(self):
        """Fixture para las pruebas."""
        print(" - Iniciando test de clases...")
        reconstruir_db()
        self.cursor = conectarse_db()

    def tearDown(self):
        """Fixture para terminar las pruebas."""
        print(" - Test de clases finalizado.")
        self.cursor.connection.close()

    def test_publicar_clase(self):
        """Este test verifica que se pueda publicar una clase."""
        
        id_act = crear_actividad(self.cursor, 'Funcional', 150.0)
        id_prof = crear_profesor(self.cursor, 'Gero', 'Arias', 'M', 6656342)
        
        res = publicar_clase(self.cursor, 'programada', id_act, id_prof)
        self.assertNotEqual(res, -1,
                    "Error al publicar la clase: se devolvió -1")
        tupla_clase = consultar_clase_por_id(self.cursor, res)
        self.assertEqual(tupla_clase[1], 'programada')
        self.assertIsNotNone(tupla_clase, "Error al consultar la clase: se devolvió None")

    def test_eliminar_clase(self):
        """Este test verifica que se pueda eliminar una clase."""

        # Crear una clase cualquiera.
        id_act = crear_actividad(self.cursor, 'Matasapos', 150.0)
        id_prof = crear_profesor(self.cursor, 'Gabriela', 'Perez', 'F', 6656343)
        res = publicar_clase(self.cursor, 'programada', id_act, id_prof)

        # Eliminar la clase creada.
        res2 = eliminar_clase_por_id(self.cursor, res)
        self.assertTrue(res2, "Error al eliminar la clase: se devolvió False")
        
        # Comprobar que no existe más en la BD.
        tupla_clase = consultar_clase_por_id(self.cursor, res)
        self.assertIsNone(tupla_clase, "Error: La clase sigue existiendo.")

    def test_modificar_clase(self):
        """Este test verifica que se pueda modificar una clase."""

        # Crear una clase cualquiera.
        id_act = crear_actividad(self.cursor, 'Snorkel', 150.0)
        id_prof = crear_profesor(self.cursor, 'Demi', 'Lovato', 'N', 6656344)
        res = publicar_clase(self.cursor, 'programada', id_act, id_prof)

        # Modificar la clase creada.
        res2 = modificar_clase(self.cursor, res, 'ocurriendo', id_act, id_prof)
        self.assertTrue(res2, "Error al modificar la clase: se devolvió False")

        # Comprobar que los cambios se efectuaron en la BD.
        tupla_clase = consultar_clase_por_id(self.cursor, res)
        self.assertEqual(tupla_clase[1], 'ocurriendo', "Error: El estado de la clase no se modificó.")

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
