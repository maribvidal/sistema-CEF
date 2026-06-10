from db.operaciones.exception_handler import ejecutar_insertar
from db import Dias

def insertar_clase(estado: str, actividad_id: int, profesor_id: int, sala_id: int, dia: Dias, hora: str, cupo_maximo: int, cursor):
    """Permite insertar una fila para la tabla Clase"""
    query = f"""INSERT INTO Clase (estado, actividad_id, profesor_id, sala_id, dia, hora, cupo_maximo)
                VALUES ('{estado}', {actividad_id}, {profesor_id}, {sala_id}, '{dia}', '{hora}', {cupo_maximo});"""
    return ejecutar_insertar(query, cursor)


## hay que ver como van a querer modelar donde van a estar las listas de espera,
## esto mover despues a donde vayan a estar

def anotarse_lista_abonados(id_usuario: int, id_clase: int, cursor):
    """Permite insertar una fila para la tabla Lista_Espera_Abonados"""
    query = f"""INSERT INTO Lista_Espera_Abonados (usuario_id, clase_id)
                VALUES ({id_usuario}, {id_clase});"""
    return ejecutar_insertar(query, cursor)

def anotarse_lista_publico_general(id_usuario: int, id_clase: int, cursor):
    """Permite insertar una fila para la tabla Lista_Espera_Publico_General"""
    query = f"""INSERT INTO Lista_Espera_Publico_General (usuario_id, clase_id)
                VALUES ({id_usuario}, {id_clase});"""
    return ejecutar_insertar(query, cursor)