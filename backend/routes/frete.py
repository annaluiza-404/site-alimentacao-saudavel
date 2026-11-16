from flask import Blueprint, jsonify, request

from services import pedido_service

bp_frete = Blueprint('frete', __name__)


@bp_frete.route('/frete', methods=['POST'])
def calcular_frete():
    dados = request.get_json(silent=True) or {}
    return jsonify({'frete': pedido_service.calcular_frete(dados.get('cep'))})


@bp_frete.route('/cupom/validar', methods=['POST'])
def validar_cupom():
    dados = request.get_json(silent=True) or {}
    frete = dados.get('frete')
    if frete is None and dados.get('cep'):
        frete = pedido_service.calcular_frete(dados.get('cep'))['valor']
    return jsonify({'cupom': pedido_service.validar_cupom(
        dados.get('codigo'), dados.get('subtotal'), frete or 0)})
