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
        "cep": dados.get('cep'),
        "cupom": dados.get('cupom')
    })
