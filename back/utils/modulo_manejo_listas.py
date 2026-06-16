from db.operaciones.clases.consultar_db import consultar_reservas_instancias_por_clase
from db.operaciones.listas_espera.consultar_db import obtener_lista_espera_abonados_por_id_clase, obtener_usuarios_lista_espera_abonados, obtener_lista_espera_individual_por_id_ins_clase, obtener_usuarios_lista_espera_individual
from utils.modulo_fechas import comprobar_fecha_anterior

"""
        - MÓDULO DE MANEJO DE LISTAS DE ESPERA -
    > Se tendría que ejecutar cada vez que se dé de baja la
    > reserva de una persona en cualquiera de las clases.
    >
    >   ------     FUNCIONAMIENTO     -----
    >
    > 1. Se revisa si hay cupos disponibles en todas las
    >    instancias de una clase. Si no hay, se termina
    >    el algoritmo.
    >
    >           En caso de que haya, se devuelve un objeto 
    >    tipo Dict donde cada item representa una instancia 
    >    de clase de id N (N > 0), y donde el valor de esta 
    >    clave es la cantidad de cupos que tenga esa 
    >    instancia de clase.
    >
    >    Ej: {"1": 2, "2": 0, ...}
    >
    > 2. Se revisa si hay gente esperando en las listas.
    >    Si no hay gente, el algoritmo termina.
    >
    >          En caso de que haya, primero se revisa si
    >    hay gente en la lista de espera de abonados, y
    >    luego se pasa a ver si hay gente en la lista de
    >    espera individual.
    >
    > 3. Si hay tanto cupos disponibles como personas
    >    esperando, entonces pueden ocurrir alguno de los
    >    siguientes escenarios:
    >
    >    3.1. Hay un cupo disponible en cada una de las
    >         instancias de la clase, y hay una persona
    >         que abonó esperando. En este caso, se crea
    >         una reserva por cada instancia de clase para
    >         el usuario que abonó.
    >
    >    3.2. Hay un cupo disponible en en cada una de las
    >         instancias de la clase, y hay una persona
    >         que NO abonó esperando. En este caso, se crea
    >         una reserva para las instancias de clase que
    >         haya reservado este usuario.
    >
    >    3.3. Hay un cupo disponible en una sola instancia y 
    >         hay una persona que abonó esperando Y una 
    >         persona que NO abonó también esperando. En este 
    >         caso, se le crea la reserva a la persona que
    >         no abonó, puesto que no hay suficientes cupos
    >         como para que la persona que abonó pueda tener
    >         una reserva en toda instancia de clase.
    >
"""

def manejar_listas_de_espera_por_clase(clase_id, cursor):
    """Función que se encarga de fijarse si hay cupos
        en una clase y las instancias de esa clase, que
        luego revisa las listas de espera asociadas a esa clase
        y, por último, decide qué acción tomar en base a esta
        información."""

    # Revisar si hay cupos disponibles.
    dict_cupos = revisar_si_hay_cupos(clase_id, cursor)
    if (not dict_cupos):
        # Los diccionarios vacíos se evalúan como falsos
        return None

    # Revisar si hay gente esperando.
    tupla_gente_esperando = revisar_gente_esperando(dict_cupos, clase_id, cursor)
    lista_abonados = tupla_gente_esperando[0]
    dict_individual = tupla_gente_esperando[1]
    if (not lista_abonados and not dict_individual):
        return None

    # Si hay cupos disponibles, enviarle a los usuarios
    # confirmaciones para cupos según alguno de los tres
    # escenarios descritos anteriormente.
        
    return (lista_abonados, dict_individual)

def revisar_si_hay_cupos(clase_id, cursor) -> dict:
    """Función que devuelve un diccionario vacío o
       lleno con pares instancia_clase-cupos."""
    
    dict_cupos = {}

    # Calcular la cantidad de cupos que hay para todas
    # las instancias de la clase.

    consulta = consultar_reservas_instancias_por_clase(clase_id, cursor)
    tuplas = consulta["data"]
    
    for tup in tuplas:
        key_name = f"{tup["inst_clase_id"]}"
        dict_cupos[key_name] = tup["cantidad_reservas"]

    return dict_cupos

def revisar_gente_esperando(dict_cupos: dict, clase_id: int, cursor) -> (list, dict):
    """Función que revisa si hay gente esperando en las listas de espera
        relacionadas con la clase recibida, y si hay, devuelve una
        tupla compuesta de una lista y un diccionario."""
    cupos_abonados = revisar_gente_esperando_lista_abonados(clase_id, cursor)
    cupos_individuales = revisar_gente_esperando_lista_individuales(dict_cupos, cursor)
    return (cupos_abonados, cupos_individuales)

def revisar_gente_esperando_lista_abonados(clase_id: int, cursor) -> list:
    consulta = obtener_lista_espera_abonados_por_id_clase(clase_id, cursor)
    id_lea = consulta["data"]["id"]
    lista_usuarios_esperando = None

    if (id_lea is not None):
        consulta2 = obtener_usuarios_lista_espera_abonados(id_lea, cursor)["data"]
        if (consulta2 is not None):
            lista_usuarios_esperando = ordenar_lista_espera_por_fecha(consulta2)

    return lista_usuarios_esperando

def revisar_gente_esperando_lista_individuales(dict_cupos: dict, cursor):
    dict_usuarios_esperando = {}
    lista_ids = obtener_lista_ids_ins_clases(dict_cupos)

    for ins_clase_id in lista_ids:
        consulta = obtener_lista_espera_individual_por_id_ins_clase(ins_clase_id, cursor)
        id_lei = consulta["data"]["id"]

        if (id_lei is not None):
            consulta2 = obtener_usuarios_lista_espera_individual(id_lei, cursor)["data"]
            if (consulta2 is not None):
                if (len(consulta2) >= 0):
                    lista_usuarios_esperando_ins_clase = ordenar_lista_espera_por_fecha(consulta2)
                    dict_usuarios_esperando[ins_clase_id] = lista_usuarios_esperando_ins_clase
    
    return dict_usuarios_esperando

def obtener_lista_ids_ins_clases(dict_cupos: list) -> list:
    lista_ids = [key for key in dict_cupos.keys()]
    return lista_ids

def ordenar_lista_espera_por_fecha(consulta) -> list:
    # Devolver los ids de los usuarios ordenados por la fecha en la cual se
    # anotaron a la lista de espera de abonados.
    lista_aux = [(tupla["usuario_id"], tupla["fecha"]) for tupla in consulta2]
    lista_aux.sort(key=lambda item: item[1])
    lista_ordenada = [item[0] for item in lista_aux]
    return lista_ordenada
