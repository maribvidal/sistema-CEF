class Restriccion:
    """Clase que representa una restricción"""

    def __init__(self, nombre: str, longitud: int):
        self.nombre = nombre
        self.longitud = longitud

    def checkear_restriccion(self, valor: str):
        """Función que comprueba que el valor de un parámetro
            no exceda la longitud indicada por la restricción."""
        if len(valor) > self.longitud:
            return {"error": f"El parámetro '{self.nombre}' no puede exceder {self.longitud} caracteres"}
        return {}

    def es_nombre(self, nombre_input: str):
        """Función que comprueba que el nombre del parámetro
            coincida con el que tiene la restricción."""
        return self.nombre == nombre_input
