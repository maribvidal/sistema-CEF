from flask import Blueprint, jsonify, request
from services.metricas_service import listar_clases_mas_canceladas_service, listar_clases_con_mensualidad_mas_concurridas_service

metricas_bp = Blueprint('metricas', __name__)

@metricas_bp.route('/metricas/clases_mas_canceladas', methods=['GET'])
def listar_clases_mas_canceladas():
    """Este endpoint permite listar todas las clases más canceladas 
        en el sistema."""
    limite = request.args.get("limite")  # Pueden ajustar el límite para mostrar mas o menos cantidad de clases en la tabla
    actividad = request.args.get("id_actividad")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    respuesta, status = listar_clases_mas_canceladas_service(limite, actividad, fecha_inicio, fecha_fin)
    
    return jsonify(respuesta), status

@metricas_bp.route('/metricas/clases_con_mensualidad', methods=['GET'])
def listar_clases_con_mensualidad_mas_concurridas():
    """Este endpoint permite listar todas las clases con mensualidad más concurridas 
        en el sistema."""
    limite = request.args.get("limite")  # Pueden ajustar el límite para mostrar mas o menos cantidad de clases en la tabla
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    respuesta, status = listar_clases_con_mensualidad_mas_concurridas_service(limite, fecha_inicio, fecha_fin)
    
    return jsonify(respuesta), status