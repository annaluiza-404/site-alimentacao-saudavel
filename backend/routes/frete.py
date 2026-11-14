from flask import Blueprint, jsonify, request

bp_frete = Blueprint('frete', __name__)

@bp_frete.route('/frete', methods=['POST'])
def calcular_frete():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "cep": dados.get('cep')
    })

@bp_frete.route('/cupom/validar', methods=['POST'])
def validar_cupom():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "codigo": dados.get('codigo'),
        "subtotal": dados.get('subtotal')
    })
