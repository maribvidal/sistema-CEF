from db.operaciones.insertar_db import insertar_usuario, insertar_profesor, insertar_actividad, insertar_mensualidad, insertar_permiso, insertar_rol

def insertar_datos():
    insertar_usuario(12345678, 'Juan', 'Pérez', '123', '2004-10-10', 'juan.perez@example.com', 1234,'masculino')
    insertar_usuario(87654321, 'María', 'Gómez', '456', '2008-07-10', 'maria.gomez@example.com', 5678,'femenino')
    insertar_profesor('Carlos', 'López', 'M', 11223344)
    insertar_profesor('Ana', 'Martínez', 'F', 44332211)
    insertar_actividad('Yoga', 50.0)
    insertar_actividad('Pilates', 60.0)
    insertar_mensualidad('2024-01-01', '2024-01-31', 1)
    insertar_mensualidad('2024-02-01', '2024-02-29', 2)
    insertar_permiso('Metricas')
    insertar_rol('Administrador')
    insertar_rol('Recepcionista')
