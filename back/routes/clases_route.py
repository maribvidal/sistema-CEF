from flask import Blueprint, request, jsonify

from services.clases_service import ( listar_clases_service )

clases_bp = Blueprint('clases', __name__)
 
@clases_bp.route('/clases', methods=['GET'])
def listar_clases():
    respuesta, status = listar_clases_service()
    
    return jsonify(respuesta), status