from flask import Blueprint, jsonify, request

bp_receitas = Blueprint('receitas', __name__)

@bp_receitas.route('/receitas', methods=['GET'])
def coletar_receitas():
    produto_id = request.args.get('produto_id')
    return jsonify({
        "produto_id": produto_id,
        "mensagem": "Rota de receitas"
    })

@bp_receitas.route('/receitas', methods=['POST'])
def criar_receita():
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "titulo": dados.get('titulo'),
        "categoria": dados.get('categoria'),
        "texto": dados.get('texto'),
        "imagem": dados.get('imagem'),
        "ingredientes": dados.get('ingredientes')
    })

@bp_receitas.route('/receitas/<int:id>', methods=['PUT'])
def atualizar_receita(id):
    dados = request.get_json(silent=True) or {}
    return jsonify({
        "receita_id": id,
        "titulo": dados.get('titulo'),
        "categoria": dados.get('categoria'),
        "texto": dados.get('texto'),
        "imagem": dados.get('imagem'),
        "ingredientes": dados.get('ingredientes')
    })

@bp_receitas.route('/receitas/<int:id>', methods=['DELETE'])
def excluir_receita(id):
    return jsonify({
        "receita_id": id,
        "mensagem": "Rota de excluir receita"
    })
