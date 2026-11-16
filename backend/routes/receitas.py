from flask import Blueprint, jsonify, request

from services import receita_service

bp_receitas = Blueprint('receitas', __name__)


@bp_receitas.route('/receitas', methods=['GET'])
def coletar_receitas():
    return jsonify({'receitas': receita_service.listar(request.args.get('produto_id'))})


@bp_receitas.route('/receitas/<int:id>', methods=['GET'])
def coletar_receita(id):
    return jsonify({'receita': receita_service.detalhar(id)})


@bp_receitas.route('/receitas', methods=['POST'])
def criar_receita():
    dados = request.get_json(silent=True) or {}
    return jsonify({'receita': receita_service.criar(dados)}), 201


@bp_receitas.route('/receitas/<int:id>', methods=['PUT'])
def atualizar_receita(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({'receita': receita_service.atualizar(id, dados)})


@bp_receitas.route('/receitas/<int:id>', methods=['DELETE'])
def excluir_receita(id):
    return jsonify(receita_service.excluir(id))
