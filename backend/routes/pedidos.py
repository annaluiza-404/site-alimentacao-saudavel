from flask import Blueprint, jsonify, request

from services import pedido_service

bp_pedidos = Blueprint('pedidos', __name__)


@bp_pedidos.route('/pedidos', methods=['GET'])
def coletar_pedidos():
    return jsonify({'pedidos': pedido_service.listar()})


@bp_pedidos.route('/pedidos/<int:id>', methods=['GET'])
def coletar_pedido(id):
    return jsonify({'pedido': pedido_service.detalhar(id)})


@bp_pedidos.route('/pedidos', methods=['POST'])
def fechar_pedido():
    dados = request.get_json(silent=True) or {}
    return jsonify({'pedido': pedido_service.fechar(dados)}), 201


@bp_pedidos.route('/pedidos/<int:id>/status', methods=['PUT'])
def atualizar_status_pedido(id):
    dados = request.get_json(silent=True) or {}
    return jsonify(pedido_service.atualizar_status(id, dados.get('status')))


@bp_pedidos.route('/pedidos/<int:id>', methods=['DELETE'])
def cancelar_pedido(id):
    return jsonify(pedido_service.cancelar(id))
