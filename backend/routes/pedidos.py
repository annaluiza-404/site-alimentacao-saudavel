from flask import Blueprint, jsonify, request

bp_pedidos = Blueprint('pedidos', __name__)

@bp_pedidos.route('/pedidos', methods=['GET'])
def coletar_pedidos():
    return jsonify({"mensagem": "Rota de pedidos"})

@bp_pedidos.route('/pedidos/<int:id>', methods=['GET'])
def coletar_pedido(id):
    return jsonify({"pedido_id": id})

@bp_pedidos.route('/pedidos', methods=['POST'])
def fechar_pedido():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "itens": dados.get('itens'),
        "endereco": dados.get('endereco'),
        "cupom": dados.get('cupom'),
        "forma_pagamento": dados.get('forma_pagamento')
    })

@bp_pedidos.route('/pedidos/<int:id>/status', methods=['PUT'])
def atualizar_status_pedido(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "pedido_id": id,
        "status": dados.get('status')
    })

@bp_pedidos.route('/pedidos/<int:id>', methods=['DELETE'])
def cancelar_pedido(id):
    return jsonify({
        "pedido_id": id,
        "mensagem": "Rota de cancelar pedido"
    })
