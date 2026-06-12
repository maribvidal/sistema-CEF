from db.operaciones.clases.consultar_db import consultar_reservas_instancias_por_clase

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
    >    de clase "ins_clase_N", y donde el valor de esta 
    >    clave es la cantidad de cupos que tenga esa 
    >    instanciade clase.
    >
    >    Ej: {"ins_clase_1": 2, "ins_clase_2": 0, ...}
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

def revisar_si_hay_cupos(clase_id, cursor) -> dict:
    """Función que devuelve un diccionario vacío o
       lleno con pares instancia_clase-cupos."""
    
    dict_cupos = {}

    # Calcular la cantidad de cupos que hay para todas
    # las instancias de la clase.

    consulta = consultar_reservas_instancias_por_clase(clase_id, cursor)

    print(consulta)

    return dict_cupos
