class restriccion:
    def __init__(self, nombre: str, longitud: int):
        self.nombre = nombre
        self.longitud = longitud
    
    # hay que modificarlo por los casos en que empieza con La en vez de El
    def checkearRestriccion(self, valor: str):
        if len(valor) > self.longitud:
            return {"error": f"El {self.nombre} no puede exceder {self.longitud} caracteres"}
        return {}

    def es_nombre(self, nombreInput: str):
        return self.nombre == nombreInput