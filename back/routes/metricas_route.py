from flask import Blueprint, jsonify, request
from services.metricas_service import listar_clases_mas_canceladas_service, listar_clases_con_mensualidad_mas_concurridas_service, listar_plata_recaudada_service, listar_plata_recaudada_service_fechas

metricas_bp = Blueprint('metricas', __name__)

@metricas_bp.route('/metricas/clases_mas_canceladas', methods=['GET'])
def listar_clases_mas_canceladas():
    """Este endpoint permite listar todas las clases más canceladas 
        en el sistema."""
    actividad = request.args.get("id_actividad")

    respuesta, status = listar_clases_mas_canceladas_service(actividad)
    
    return jsonify(respuesta), status

@metricas_bp.route('/metricas/clases_mas_canceladas/con_fechas', methods=['GET'])
def listar_clases_mas_canceladas_fechas():
    """Este endpoint permite listar todas las clases más canceladas 
        en el sistema."""
    actividad = request.args.get("id_actividad")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    respuesta, status = listar_clases_mas_canceladas_service(actividad, fecha_inicio, fecha_fin)
    
    return jsonify(respuesta), status

@metricas_bp.route('/metricas/clases_con_mensualidad', methods=['GET'])
def listar_clases_con_mensualidad_mas_concurridas():
    """Este endpoint permite listar todas las clases con mensualidad más concurridas 
        en el sistema."""

    respuesta, status = listar_clases_con_mensualidad_mas_concurridas_service()
    
    return jsonify(respuesta), status

@metricas_bp.route('/metricas/clases_con_mensualidad/con_fechas', methods=['GET'])
def listar_clases_con_mensualidad_mas_concurridas_fechas():
    """Este endpoint permite listar todas las clases con mensualidad más concurridas 
        en el sistema."""
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    respuesta, status = listar_clases_con_mensualidad_mas_concurridas_service(fecha_inicio, fecha_fin)
    
    return jsonify(respuesta), status

@metricas_bp.route('/metricas/plata_recaudada', methods=['GET'])
def listar_plata_recaudada():
    """Este endpoint permite listar la plata recaudada en el sistema."""

    respuesta, status = listar_plata_recaudada_service()

    return jsonify(respuesta), status

@metricas_bp.route('/metricas/plata_recaudada/con_fechas', methods=['GET'])
def listar_plata_recaudada_fechas():
    """Este endpoint permite listar la plata recaudada en el sistema."""
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    respuesta, status = listar_plata_recaudada_service_fechas(fecha_inicio, fecha_fin)

    return jsonify(respuesta), status