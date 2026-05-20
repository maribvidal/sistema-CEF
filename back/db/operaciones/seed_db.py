from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.profesores.insertar_db import insertar_profesor
from db.operaciones.actividades.insertar_db import insertar_actividad
from db.operaciones.mensualidades.insertar_db import insertar_mensualidad
from db.operaciones.permisos.insertar_db import insertar_permiso
from db.operaciones.roles.insertar_db import insertar_rol
from db.operaciones import insertar_pago, insertar_clase
from db.operaciones import insertar_pago_pagar_clase

def insertar_datos():   
    insertar_usuario(12345678, 'Juan', 'Pérez', '123', '2004-10-10', 'juan.perez@example.com', 1234,'M')
    insertar_usuario(12345678, 'María', 'Gómez', '456', '2008-07-10', 'maria.gomez@example.com', 5678,'F')
    insertar_profesor('Carlos', 'López', 'M', 11223344)
    insertar_profesor('Ana', 'Martínez', 'F', 44332211)
    insertar_actividad('Yoga', 50.0)
    insertar_actividad('Pilates', 60.0)
    #insertar_mensualidad('2024-01-01', '2024-31-01', 1)
    #insertar_mensualidad('2024-02-02', '2024-29-02', 2)
    insertar_permiso('Metricas')
    insertar_rol('Administrador')
    insertar_rol('Recepcionista')
    insertar_clase('Programada', 1, 1)
    insertar_pago(50.0, 1)
    insertar_pago(60.0, 2)
    insertar_pago_pagar_clase(1, 1)
