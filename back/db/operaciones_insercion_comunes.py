import sqlite3 as sqlite

from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.profesores.insertar_db import insertar_profesor

# Estas operaciones devuelven el id de la fila insertada si hubo 
# éxito, o -1 si hubo un error.

def crear_actividad(cursor: sqlite.Cursor, nombre: str, precio_mensual: float) -> int:
    """Función que se encarga de insertar una actividad y controlar
        algunas cuestiones mas."""
    try:
        return insertar_actividad(cursor, nombre, precio_mensual)
    except sqlite.IntegrityError as e:
        print(f" > Error al crear actividad: Actividad '{nombre}' ya existe. Detalles: {e}")
        return -1
    except Exception as e:
        print(f" > Error al crear actividad: {e}")
        return -1

def crear_profesor(cursor: sqlite.Cursor, nombre: str, apellido: str, genero: str, dni: int) -> int:
    """Función que se encarga de insertar un profesor y controlar
        algunas cuestiones mas."""
    try:
        return insertar_profesor(cursor, nombre, apellido, genero, dni)
    except sqlite.IntegrityError as e:
        print(f" > Error al crear profesor: DNI {dni} ya existe. Detalles: {e}")
        return -1
    except Exception as e:
        print(f" > Error al crear profesor: {e}")
        return -1

def publicar_clase(cursor: sqlite.Cursor, estado: str, actividad_id: int, profesor_id: int) -> int:
    """Función que se encarga de insertar una clase y controlar
        algunas cuestiones mas."""
    try:
        return insertar_clase(cursor, estado, actividad_id, profesor_id)
    except sqlite.IntegrityError as e:
        print(f" > Error al publicar clase: Error de integridad. Detalles: {e}")
        if ("FOREIGN KEY constraint failed" in str(e)):
            print("   - Verifique que el ID de actividad y profesor existan.")
        return -1
    except Exception as e:
        print(f" > Error al publicar clase: {e}")
        return -1
