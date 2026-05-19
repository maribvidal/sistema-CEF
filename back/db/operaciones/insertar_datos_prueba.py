from db.operaciones.insertar_db import insertar_usuario, insertar_profesor, insertar_actividad, insertar_mensualidad, insertar_permiso, insertar_rol

def insertar_datos():
    #insertar_usuario(12345678, 'Juan', 'Pérez', '2002-01-01', '123', 'juan.perez@example.com', 1234,'masculino')
    #insertar_usuario(87654321, 'María', 'Gómez', '2002-01-01', '456', 'maria.gomez@example.com', 5678,'femenino')
    insertar_profesor('Carlos', 'López', 'M', 11223344)
    insertar_profesor('Ana', 'Martínez', 'F', 44332211)
    insertar_actividad('Yoga', 50.0)
    insertar_actividad('Pilates', 60.0)
    #insertar_mensualidad('2024-01-01', '2024-31-01', 1)
    #insertar_mensualidad('2024-02-02', '2024-29-02', 2)
    insertar_permiso('Metricas')
    insertar_rol('Administrador')
    insertar_rol('Recepcionista')
