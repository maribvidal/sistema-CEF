from flask import Blueprint, request, jsonify

from services.clases_service import ( publicar_clase_service,cancelar_clase_service, eliminar_clases_service, listar_clases_service, modificar_clase_service )

clases_bp = Blueprint('clases', __name__)
 
@clases_bp.route('/clases', methods=['GET'])
def listar_clases():
    respuesta, status = listar_clases_service()
    
    return jsonify(respuesta), status