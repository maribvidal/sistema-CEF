class Restriccion:
    """Clase que representa una restricción"""

    def __init__(self, nombre: str, longitud = None, funcion_checkeo = None):
        self.nombre = nombre
        self.longitud = longitud
        self.funcion_checkeo = funcion_checkeo

    def checkear(self, valor):
        """Ejecuta todas las validaciones de la restricción."""

        if self.longitud is not None and len(valor) > self.longitud:
            return {
                "error": f"El parámetro '{self.nombre}' no puede exceder {self.longitud} caracteres"
            }

        if self.funcion_checkeo is not None:
            return self.funcion_checkeo(valor)

        return {}

    def es_nombre(self, nombre_input: str) -> bool:
        """Función que comprueba que el nombre del parámetro
            coincida con el que tiene la restricción."""
        return self.nombre == nombre_input
