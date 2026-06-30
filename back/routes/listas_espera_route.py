from flask import Blueprint, request, jsonify

listas_espera_bp = Blueprint('listas_espera', __name__)

@listas_espera_bp.route('/lista_espera_abonados/confirmar', methods=['POST'])
def confirmar_lista_espera_abonados():
    data = request.get_json()
    dni_cliente = data.get('dni_cliente')
    clase_id = data.get('clase_id')

    respuesta, status = agregar_usuario_a_lista_espera_abonados(dni_cliente, clase_id)
    return jsonify(respuesta), status