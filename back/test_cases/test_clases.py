import unittest

from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.consultar_db import consultar_clase_por_id
from db.operaciones.clases.modificar_db import modificar_clase
from db.operaciones.clases.borrar_db import borrar_clase

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
        
        id_act = insertar_actividad('Funcional', 150.0, self.cursor)
        id_prof = insertar_profesor('Gero', 'Arias', 'M', 6656342, self.cursor)
        
        res = insertar_clase(self.cursor, 'programada', id_act["data"], id_prof["data"])

        self.assertEqual(res["status"], "success", "No se pudo publicar la clase.")

        # Consultar la clase y extraer el registro en distintos formatos.
        tupla_clase = consultar_clase_por_id(res["data"], self.cursor)
        if isinstance(tupla_clase, dict):
            self.assertEqual(tupla_clase.get('status'), 'success', f"Error al consultar la clase: {tupla_clase}")
            datos = tupla_clase.get('data')
            registro = datos[0] if isinstance(datos, list) and datos else datos
        else:
            registro = tupla_clase

        self.assertIsNotNone(registro, "Error al consultar la clase: se devolvió None")
        self.assertEqual(registro[1], 'programada')

    def test_eliminar_clase(self):
        """Este test verifica que se pueda eliminar una clase."""

        # Crear una clase cualquiera.
        id_act = insertar_actividad('Matasapos', 150.0, self.cursor)
        id_prof = insertar_profesor('Gabriela', 'Perez', 'F', 6656343, self.cursor)
        res = insertar_clase('programada', id_act["data"], id_prof["data"], self.cursor)
        if isinstance(res, dict):
            self.assertEqual(res.get('status'), 'success', f"Error al publicar la clase: {res}")
            res = res.get('data')

        # Eliminar la clase creada.
        res2 = borrar_clase(res, self.cursor)
        self.assertTrue(res2, "Error al eliminar la clase: se devolvió False")
        
        # Comprobar que no existe más en la BD.
        tupla_clase = consultar_clase_por_id(res, self.cursor)
        if isinstance(tupla_clase, dict):
            # Si la consulta devuelve estructura, comprobar data vacía o None
            self.assertTrue(tupla_clase.get('data') in (None, [], {}), "Error: La clase sigue existiendo.")
        else:
            self.assertIsNone(tupla_clase, "Error: La clase sigue existiendo.")

    def test_modificar_clase(self):
        """Este test verifica que se pueda modificar una clase."""

        # Crear una clase cualquiera.
        id_act = insertar_actividad('Snorkel', 150.0, self.cursor)
        id_prof = insertar_profesor('Demi', 'Lovato', 'N', 6656344, self.cursor)
        res = insertar_clase('programada', id_act["data"], id_prof["data"], self.cursor)
        if isinstance(res, dict):
            self.assertEqual(res.get('status'), 'success', f"Error al publicar la clase: {res}")
            res = res.get('data')

        # Modificar la clase creada.
        res2 = modificar_clase(self.cursor, res, 'ocurriendo', id_act["data"], id_prof["data"])
        self.assertTrue(res2, "Error al modificar la clase: se devolvió False")

        # Comprobar que los cambios se efectuaron en la BD.
        tupla_clase = consultar_clase_por_id(res, self.cursor)
        if isinstance(tupla_clase, dict):
            self.assertEqual(tupla_clase.get('status'), 'success', f"Error al consultar la clase: {tupla_clase}")
            datos = tupla_clase.get('data')
            registro = datos[0] if isinstance(datos, list) and datos else datos
        else:
            registro = tupla_clase

        self.assertIsNotNone(registro, "Error al consultar la clase después de modificarla: se devolvió None")
        self.assertEqual(registro[1], 'ocurriendo', "Error: El estado de la clase no se modificó.")

if __name__ == '__main__':
    unittest.main()
