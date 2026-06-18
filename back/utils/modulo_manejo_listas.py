from db.operaciones.clases.consultar_db import consultar_reservas_instancias_por_clase, consultar_clase_por_id
from db.operaciones.listas_espera.consultar_db import obtener_lista_espera_abonados_por_id_clase, obtener_usuarios_lista_espera_abonados, obtener_lista_espera_individual_por_id_ins_clase, obtener_usuarios_lista_espera_individual
from db.operaciones.usuario_pertenece_lista_espera_abonados.borrar_db import borrar_usuario_pertenece_lista_espera_abonados_por_id, borrar_usuario_pertenece_lista_espera_individual_por_id
from db.operaciones.reservas.insertar_db import insertar_reserva

from utils.modulo_fechas import comprobar_fecha_anterior
from utils.envio_mails import enviar_mail_confirmacion_asistencia

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

    # Escenario 3.1

    if (lista_abonados):
        manejar_cupos_disponibles_abonados(clase_id, lista_abonados, dict_cupos, cursor)

    # Escenario 3.2

    if (dict_individual):
        manejar_cupos_disponibles_individuales(dict_cupos, dict_individual, cursor)
        
    return (lista_abonados, dict_individual)

def revisar_si_hay_cupos(clase_id, cursor) -> dict:
    """Función que devuelve un diccionario vacío o
       lleno con pares instancia_clase-cupos."""
    
    dict_cupos = {}

    # Obtener el cupo máximo de la clase.

    consulta = consultar_clase_por_id(clase_id, cursor)
    cupo_maximo = consulta["data"]["cupo_maximo"]

    # Calcular la cantidad de cupos que hay para todas
    # las instancias de la clase.

    consulta2 = consultar_reservas_instancias_por_clase(clase_id, cursor)
    tuplas = consulta2["data"]
    
    for tup in tuplas:
        key_name = f"{tup["inst_clase_id"]}"
        dict_cupos[key_name] = cupo_maximo - tup["cantidad_reservas"]

    return dict_cupos

def manejar_cupos_disponibles_abonados(clase_id, lista_abonados, dict_cupos, cursor):
    """Función que se encarga de manejar el tema de los cupos para
        los abonados."""
    id_lea = obtener_lista_espera_abonados_por_id_clase(clase_id, cursor)["data"]["id"]
    cupos_disponibles_abonado = revisar_cupos_disponible_abonado(dict_cupos)
    if (cupos_disponibles_abonado > 0):
        avisar_abonados(id_lea, lista_abonados, cupos_disponibles_abonado, cursor)

def manejar_cupos_disponibles_individuales(dict_cupos, dict_individual, cursor):
    """Función que se encarga de manejar el tema de los cupos para
        las personas que pagaron la clase de forma individual."""
    lista_ids = obtener_lista_ids_ins_clases(dict_cupos)
    for item in lista_ids:
        cupos_disponibles_inviduales = dict_cupos[item]
        lista_individuales_ins_clase = dict_individual[item]
        gente_esperando = len(lista_individuales_ins_clase)

        if (cupos_disponibles_inviduales > 0):

    while (cant_cupos > 0 and gente_esperando > 0):
        id_individual = lista_individuales.pop(0)
        # Quizás no habría que quitar a los usuarios de la 
        # lista de espera en este momento, pero después lo veo mejor.
        cons = borrar_usuario_pertenece_lista_espera_abonados_por_id(id_lea, id_abonado, cursor)
        cant_abonados_esperando = len(lista_abonados)
        cursor.connection.commit()
        # Enviarle un email para que pueda confirmar su asistencia
        enviar_mail_confirmacion_asistencia(id_abonado, cursor)
        # Restar un cupo disponible (igualmente, si el usuario
        # cancela, entonces ese cupo va a volver a estar disponible.)
        cupos_disp -= 1


    cupos_disponibles_abonado = revisar_cupos_disponible_abonado(dict_cupos)
    if (cupos_disponibles_abonado > 0 and lista_abonados):
        avisar_abonados(id_lea, lista_abonados, cupos_disponibles_abonado, cursor)

def revisar_cupos_disponible_abonado(dict_cupos: dict) -> bool:
    """Función que itera sobre todas las instancias de clases que
        figuran en dict_cupos, y comprueba que en todas haya
        por lo menos 1 cupo."""
    cant_ins_clases = len(dict_cupos)
    cant_ins_clases_con_1_cupo = 0

    for ins_clase in dict_cupos:
        if dict_cupos[ins_clase] > 0:
            cant_ins_clases_con_1_cupo += 1

    hay_cupos = cant_ins_clases_con_1_cupo > 0
    hay_para_toda_ins_clase = cant_ins_clases_con_1_cupo == cant_ins_clases

    return hay_cupos and hay_para_toda_ins_clase

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
    lista_aux = [(tupla["usuario_id"], tupla["fecha"]) for tupla in consulta]
    lista_aux.sort(key=lambda item: item[1])
    lista_ordenada = [item[0] for item in lista_aux]
    return lista_ordenada

def avisar_abonados(id_lea: int, lista_abonados: list, cupos_disp: int, cursor):
    """Función que le envía un mail a cada abonado que estaba
        esperando en la lista por esa clase, mientras hayan
        cupos disponibles."""
    cant_abonados_esperando = len(lista_abonados)

    while (cant_abonados_esperando > 0 and cupos_disp > 0):
        # Quitar un usuario de la lista
        id_abonado = lista_abonados.pop(0)
        # Quizás no habría que quitar a los usuarios de la 
        # lista de espera en este momento, pero después lo veo mejor.
        cons = borrar_usuario_pertenece_lista_espera_abonados_por_id(id_lea, id_abonado, cursor)
        cant_abonados_esperando = len(lista_abonados)
        cursor.connection.commit()
        # Enviarle un email para que pueda confirmar su asistencia
        enviar_mail_confirmacion_asistencia(id_abonado, cursor)
        # Restar un cupo disponible (igualmente, si el usuario
        # cancela, entonces ese cupo va a volver a estar disponible.)
        cupos_disp -= 1
